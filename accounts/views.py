from django.shortcuts import redirect, render
from django.views.generic import View
from accounts.forms import BrandProfileForm, BrandSignUpForm, ProfileForm, SignInForm
from django.core.mail import send_mail
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def send_otp_email(user):
    
    user.generate_otp()
    subject = 'CollabX - Email Verification'
    message = f'Your OTP for Email verification is: {user.otp}'
    from_email = 'iamrbn03@gmail.com'
    to_email = [user.email]
    
    send_mail(subject, message, from_email, to_email)


class BrandSignUpView(View):
    
    template_name = 'brand_signup.html'
    form_class = BrandSignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form': form,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            # form.instance.is_brand = True
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            user_obj.save()
            send_otp_email(user_obj)    
            
            return redirect('verify-email')
        
        context = {
            'form': form,
        }
        
        print('Failed to create brand user!')
        return render(request, self.template_name, context)
    

class VerifyEmailView(View):
    
    template_name = 'verify_email.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        
        otp = request.POST.get('otp')

        try:
            user_obj = User.objects.get(otp=otp)
            user_obj.is_active = True
            user_obj.otp = None
            user_obj.save()
            
            if user_obj.is_brand:
                return redirect('create-brand-profile')
            else:
                pass
            
        except:
            messages.error(request, 'Invalid OTP')
            return render(request, self.template_name)
        
        
class SignInView(View):
    
    template_name = 'signin.html'
    form_class = SignInForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            
            user_obj = authenticate(request, username=uname, password=pwd)
            

            
            if user_obj:
                
                login(request, user_obj)
                return redirect('home')
            
        return render(request, self.template_name, {'form':form})
        
        
class BrandProfileCreateView(View):
    
    template_name = 'brand_profile_form.html'
    profile_form_class = ProfileForm
    brand_form_class = BrandProfileForm
    
    def get(self, request, *args, **kwargs):
        
        profile_form = self.profile_form_class()
        brand_form = self.brand_form_class()
        
        context = {
            'profile_form': profile_form,
            'brand_form': brand_form,
        }
        
        return render(request, self.template_name, context)
        
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        files = request.FILES
        
        profile_form = self.profile_form_class(form_data, files)
        brand_form = self.brand_form_class(form_data)
        
        if profile_form.is_valid() and brand_form.is_valid():
            
            profile = profile_form.save(commit=False)
            profile.owner = request.user
            profile_form.save()
            brand_profile = brand_form.save(commit=False)
            brand_profile.profile_object = profile
            brand_form.save()
            return redirect('home')
            
        return render(request, self.template_name)