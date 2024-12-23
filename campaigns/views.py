from django.shortcuts import redirect, render
from django.views.generic import View
from campaigns.forms import CampaignForm
from campaigns.models import Campaign, Proposal

# Create your views here.

class IndexView(View):
    
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    
    
class BrandDashboardView(View):
    
    template_name = 'brand_dashboard.html'
    
    def get(self, request, *args, **kwargs):
        
        context = {}
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
        user_proposal = Proposal.objects.filter(campaign_object=qs, creator_object=request.user.profile.creator_profile).first()
        
        context = {
            'campaign':qs,
            'user_proposal': user_proposal,
        }

        return render(request, self.template_name, context)
    
    
class CreatorDashbaordView(View):
    
    template_name = 'creator_dashboard.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    


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
        
        id = kwargs.get('id')
        proposal = Proposal.objects.get(id=id)
        proposal.status = 'accepted'
        proposal.save()
        return redirect('campaign-detail', pk=proposal.campaign.id)


class RejectProposalView(View):
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('id')
        proposal = Proposal.objects.get(id=id)
        proposal.status = 'rejected'
        proposal.save()
        return redirect('campaign-detail', pk=proposal.campaign.id)