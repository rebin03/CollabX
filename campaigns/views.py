from django.shortcuts import redirect, render
from django.views.generic import View
from campaigns.forms import CampaignForm, ReportForm
from campaigns.models import Campaign, DismissedNotification, EscrowTransaction, Proposal, Rating
from django.db.models import Avg
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import razorpay

RAZORPAY_KEY_ID = config('RZP_KEY_ID')
RAZORPAY_KEY_SECRET = config('RZP_KEY_SECRET')

# Create your views here.

class IndexView(View):
    
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    
    
class BrandDashboardView(View):
    
    template_name = 'brand_dashboard.html'
    
    def get(self, request, *args, **kwargs):
        
        brand_profile = request.user.profile.brand_profile
        campaigns = brand_profile.campaigns.all()
        total_campaigns = campaigns.count()
        active_collaborations = campaigns.filter(status='active').count()
        pending_proposals = Proposal.objects.filter(campaign_object__in=campaigns, status='pending').count()
        average_rating = Rating.objects.filter(proposal__campaign_object__in=campaigns).aggregate(Avg('rating'))['rating__avg'] or 0

        # Filter accepted proposals
        accepted_proposals = Proposal.objects.filter(campaign_object__in=campaigns, status__in=['accepted', 'working', 'submitted'])
        completed_proposals = Proposal.objects.filter(campaign_object__in=campaigns, status='completed')
        past_campaigns = campaigns.filter(status='completed')

        context = {
            'campaigns': campaigns,
            'total_campaigns': total_campaigns,
            'active_collaborations': active_collaborations,
            'pending_proposals': pending_proposals,
            'average_rating': round(average_rating, 1),
            'accepted_proposals': accepted_proposals,
            'completed_proposals': completed_proposals,
            'past_campaigns': past_campaigns,
        }
        
        return render(request, self.template_name, context)
    
    
class CreateCampaignView(View):
    
    template_name = 'add_campaign.html'
    form_class = CampaignForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        print(request.user)
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        files = request.FILES
        
        form = self.form_class(form_data, files)
        
        if form.is_valid():
            
            campaign_object = form.save(commit=False)
            campaign_object.brand = request.user.profile.brand_profile
            form.save()
            # saving many-to-many field
            form.save_m2m()
            
            return redirect('brand-dashboard')
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    

class CampaignListView(View):
    
    template_name = 'campaign_list.html'

    def get(self, request, *args, **kwargs):
        brand_type = request.GET.getlist('brand_type')
        content_type = request.GET.getlist('content_type')
        audience_type = request.GET.getlist('audience_type')
        min_budget = request.GET.get('min_budget')
        max_budget = request.GET.get('max_budget')

        campaigns = Campaign.objects.exclude(status__in=['completed', 'closed'])

        if brand_type:
            campaigns = campaigns.filter(brand__brand_type__in=brand_type)
        
        if content_type:
            campaigns = campaigns.filter(content_types__name__in=content_type).distinct()
        
        if audience_type:
            campaigns = campaigns.filter(audience_preferences__name__in=audience_type).distinct()
        
        if min_budget and max_budget:
            campaigns = campaigns.filter(budget__gte=min_budget, budget__lte=max_budget)

        context = {
            'campaigns': campaigns,
            'selected_brand_type': brand_type,
            'selected_content_type': content_type,
            'selected_audience_type': audience_type,
            'min_budget': min_budget,
            'max_budget': max_budget,
        }
        
        return render(request, self.template_name, context)


class CampaignDetailView(View):
    
    template_name = 'campaign_detail.html'

    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        qs = Campaign.objects.get(id=id)
        user_proposal = None

        if hasattr(request.user.profile, 'creator_profile'):
            user_proposal = Proposal.objects.filter(campaign_object=qs, creator_object=request.user.profile.creator_profile).first()
        
        context = {
            'campaign':qs,
            'user_proposal': user_proposal,
        }

        return render(request, self.template_name, context)
    
    
class UpdateCampaignView(View):
    
    template_name = 'edit_campaign.html'
    form_class = CampaignForm
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=id)
        form = self.form_class(instance=campaign)
        
        context = {
            'form': form,
            'campaign': campaign,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=id)
        form = self.form_class(request.POST, request.FILES, instance=campaign)
        
        if form.is_valid():
            form.save()
            return redirect('brand-dashboard')
        
        context = {
            'form': form,
            'campaign': campaign,
        }
        
        return render(request, self.template_name, context)


class DeleteCampaignView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=id)
        campaign.delete()
        return redirect('brand-dashboard')



class ViewReportView(View):
    
    template_name = 'view_report.html'
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(id=id)
        
        context = {
            'proposal': proposal,
        }
        
        return render(request, self.template_name, context)
    
    
class CompleteCampaignView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=id)
        campaign.status = 'completed'
        campaign.save()
        
        return redirect('brand-dashboard')
    
    
class CreatorDashbaordView(View):
    
    template_name = 'creator_dashboard.html'

    def get(self, request, *args, **kwargs):
        
        creator_profile = request.user.profile.creator_profile
        active_campaigns = Campaign.objects.filter(
            proposals__creator_object=creator_profile,
            proposals__status__in=['accepted', 'working', 'submitted'],
            status='active'
        )
        completed_campaigns = Campaign.objects.filter(
            proposals__creator_object=creator_profile,
            proposals__status='completed'
        )
        active_campaigns_count = active_campaigns.count()
        pending_proposals_count = Proposal.objects.filter(creator_object=creator_profile, status='pending').count()
        completed_proposals_count = Proposal.objects.filter(creator_object=creator_profile, status='completed').count()
        requested_campaigns = Proposal.objects.filter(creator_object=creator_profile).select_related('campaign_object')
        
        # Get dismissed notifications from session
        dismissed_notifications = DismissedNotification.objects.filter(user=request.user).values_list('proposal_id', flat=True)

        # Filter out dismissed notifications
        notifications = requested_campaigns.exclude(id__in=dismissed_notifications).filter(status__in=['rejected', 'accepted'])
        notification_count = notifications.count()
        
        context = {
            'active_campaigns': active_campaigns,
            'completed_campaigns': completed_campaigns,
            'pending_proposals_count': pending_proposals_count,
            'completed_proposals_count': completed_proposals_count,
            'requested_campaigns': requested_campaigns,
            'active_campaigns_count': active_campaigns_count,
            'notifications': notifications,
            'notification_count': notification_count,
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        # Handle dismissing notifications
        notification_id = request.POST.get('notification_id')
        if notification_id:
            proposal = Proposal.objects.get(id=notification_id)
            DismissedNotification.objects.create(user=request.user, proposal=proposal)
        return redirect('creator-dashboard')
    


class SubmitProposalView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=id)
        creator = request.user.profile.creator_profile
        message = request.POST.get('message')
        
        proposal = Proposal.objects.create(
            campaign_object=campaign,
            creator_object=creator,
            message=message,
            is_interested=True,
            status='pending'
        )
        return redirect('campaign-detail', pk=id)


class CancelProposalView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(id=id)
        proposal.delete()
        return redirect('campaign-detail', pk=proposal.campaign_object.id)


class AcceptProposalView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(id=id)
        proposal.status = 'accepted'
        proposal.save()
        
        # Set the campaign status to 'active'
        campaign = proposal.campaign_object
        campaign.status = 'active'
        campaign.save()
        
        # Create Razorpay order
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order_amount = int(campaign.budget * 100)  # Convert to paise
        order_currency = 'INR'
        order_receipt = f'order_rcptid_{proposal.id}'
        notes = {'proposal_id': proposal.id}
        
        try:
            order = client.order.create({
                'amount': order_amount,
                'currency': order_currency,
                'receipt': order_receipt,
                'notes': notes
            })
        except Exception as e:
            return render(request, 'payment_error.html', {'error': 'Error creating Razorpay order.'})
        
        # Create EscrowTransaction
        escrow_transaction = EscrowTransaction.objects.create(
            proposal=proposal,
            amount=campaign.budget,
            razorpay_order_id=order.get('id')
        )
        
        context = {
            'order_id': order.get('id'),
            'amount': order_amount,
            'currency': order_currency,
            'razorpay_key_id': RAZORPAY_KEY_ID,
            'proposal': proposal,
            'escrow_transaction': escrow_transaction
        }
        
        return render(request, 'payment.html', context)
    

class StartWorkingView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(campaign_object_id=id, creator_object=request.user.profile.creator_profile)
        proposal.status = 'working'
        proposal.save()
        
        return redirect('creator-dashboard')
    

class SubmitReportView(View):
    
    template_name = 'submit_report.html'
    form_class = ReportForm
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(campaign_object_id=id, creator_object=request.user.profile.creator_profile)
        form = self.form_class(instance=proposal)
        
        context = {
            'form': form,
            'proposal': proposal,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(campaign_object_id=id, creator_object=request.user.profile.creator_profile)
        form = self.form_class(request.POST, request.FILES, instance=proposal)
        
        if form.is_valid():
            proposal.status = 'submitted'
            form.save()
            return redirect('creator-dashboard')
        
        context = {
            'form': form,
            'proposal': proposal,
        }
        
        return render(request, self.template_name, context)


class ReviewReportView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(id=id)
        action = request.POST.get('action')
        
        if action == 'accept':
            proposal.status = 'completed'
            proposal.save()
            
            # Release payment to the creator
            escrow_transaction = proposal.escrow_transaction
            escrow_transaction.status = 'completed'
            escrow_transaction.save()
        
        elif action == 'reject':
            proposal.status = 'working'
            proposal.save()
        
        return redirect('brand-dashboard')
   

@method_decorator(csrf_exempt, name='dispatch')
class PaymentCallbackView(View):
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        
        try:
            client.utility.verify_payment_signature(data)
            escrow_transaction = EscrowTransaction.objects.get(razorpay_order_id=data['razorpay_order_id'])
            escrow_transaction.razorpay_payment_id = data['razorpay_payment_id']
            escrow_transaction.razorpay_signature = data['razorpay_signature']
            # escrow_transaction.status = 'pending'
            escrow_transaction.save()
            return JsonResponse({'status': 'success'})
        
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'failure'})



class RejectProposalView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        proposal = Proposal.objects.get(id=id)
        proposal.status = 'rejected'
        proposal.save()
        return redirect('pending-proposals')
    
    
class PendingProposalsView(View):
    
    template_name = 'pending_proposals.html'
    
    def get(self, request, *args, **kwargs):
        brand_profile = request.user.profile.brand_profile
        pending_proposals = Proposal.objects.filter(campaign_object__brand=brand_profile, status='pending')
        
        context = {
            'pending_proposals': pending_proposals,
        }
        
        return render(request, self.template_name, context)
    
    
class InvoiceView(View):
    
    template_name = 'invoice.html'
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        campaign = Campaign.objects.get(id=id)
        proposal = Proposal.objects.filter(campaign_object=campaign, creator_object=request.user.profile.creator_profile).first()
        escrow_transaction = proposal.escrow_transaction
        
        context = {
            'campaign': campaign,
            'proposal': proposal,
            'escrow_transaction': escrow_transaction,
        }
        
        return render(request, self.template_name, context)