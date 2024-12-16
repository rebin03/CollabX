from django.shortcuts import redirect, render
from django.views.generic import View
from campaigns.forms import CampaignForm

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