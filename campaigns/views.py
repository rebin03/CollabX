from django.shortcuts import redirect, render
from django.views.generic import View
from campaigns.forms import CampaignForm
from campaigns.models import Campaign, Proposal, Rating
from django.db.models import Avg

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
        accepted_proposals = Proposal.objects.filter(campaign_object__in=campaigns, status='accepted')

        context = {
            'campaigns': campaigns,
            'total_campaigns': total_campaigns,
            'active_collaborations': active_collaborations,
            'pending_proposals': pending_proposals,
            'average_rating': round(average_rating, 1),
            'accepted_proposals': accepted_proposals,
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
        
        qs = Campaign.objects.all()
        
        context = {
            'campaigns':qs
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
    
    
class CreatorDashbaordView(View):
    
    template_name = 'creator_dashboard.html'

    def get(self, request, *args, **kwargs):
        
        creator_profile = request.user.profile.creator_profile
        active_campaigns = Campaign.objects.filter(proposals__creator_object=creator_profile, proposals__status='accepted', status='active')
        active_campaigns_count = active_campaigns.count()
        pending_proposals_count = Proposal.objects.filter(creator_object=creator_profile, status='pending').count()
        requested_campaigns = Proposal.objects.filter(creator_object=creator_profile).select_related('campaign_object')
        
        # Get dismissed notifications from session
        dismissed_notifications = request.session.get('dismissed_notifications', [])

        # Filter out dismissed notifications
        notifications = requested_campaigns.exclude(id__in=dismissed_notifications)
        
        context = {
            'active_campaigns': active_campaigns,
            'pending_proposals_count': pending_proposals_count,
            'requested_campaigns': requested_campaigns,
            'active_campaigns_count': active_campaigns_count,
            'notifications': notifications,
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        # Handle dismissing notifications
        notification_id = request.POST.get('notification_id')
        if notification_id:
            dismissed_notifications = request.session.get('dismissed_notifications', [])
            dismissed_notifications.append(int(notification_id))
            request.session['dismissed_notifications'] = dismissed_notifications
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
        
        return redirect('pending-proposals')


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