from django.shortcuts import redirect, render
from django.views.generic import View
from accounts.forms import BrandProfileForm, BrandSignUpForm, CreatorProfileForm, CreatorSignUpForm, ProfileForm, SignInForm
from django.core.mail import send_mail
from accounts.models import Niche, Platform, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

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
        
        messages.error(request, 'Invalid types in fields or mismatch in re-entered passwords')
        return render(request, self.template_name, context)
    
    
class CreatorSignUpView(View):
    
    template_name = 'creator_signup.html'
    form_class = CreatorSignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            user_obj.save()
            send_otp_email(user_obj)    
            
            return redirect('verify-email')
        
        context = {
            'form': form,
        }
        
        print('Failed to create creator user!')
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
            return redirect('signin')
            
        except User.DoesNotExist:
            messages.error(request, 'Invalid OTP or User does not exist')
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
                if user_obj.is_active:
                    login(request, user_obj)
                    print("User Object Authenticated:", user_obj.is_authenticated)
                    print("Is user authenticated?", request.user.is_authenticated)
                    print("Logged in User:", request.user)

                    if user_obj.is_brand:
                        # Check if the user has a profile
                        if request.user.has_profile:
                            return redirect('home')
                        else:
                            return redirect('create-brand-profile')
                    else:
                        if request.user.has_profile:
                            return redirect('home')
                        else:
                            print("Session Key Before:", request.session.session_key)
                            return redirect('create-creator-profile')
                
                messages.error(request, 'Your email is not verified')
            messages.error(request, 'Invalid credentials')      
        return render(request, self.template_name, {'form':form})
        
 
class SignOutView(View):
    
    def get(self, request, *args, **kwargs):
        
        logout(request)    
        return redirect('home')
 
        
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
            return redirect('brand-dashboard')
            
        context = {
            'profile_form': profile_form,
            'brand_form': brand_form,
        }
        
        return render(request, self.template_name, context)
    

class CreatorProfileCreateView(View):
    
    template_name = 'creator_profile_form.html'
    profile_form_class = ProfileForm
    creator_form_class = CreatorProfileForm
    
    def get(self, request, *args, **kwargs):
        
        profile_form = self.profile_form_class()
        creator_form = self.creator_form_class()
        print("Session Key After:", request.session.session_key)
        print(request.user)
        
        context = {
            'profile_form': profile_form,
            'creator_form': creator_form,
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        files = request.FILES
        
        profile_form = self.profile_form_class(form_data, files)
        creator_form = self.creator_form_class(form_data)

        if profile_form.is_valid() and creator_form.is_valid():
            
            profile = profile_form.save(commit=False)
            profile.owner = request.user
            profile_form.save()
            creator_profile = creator_form.save(commit=False)
            creator_profile.profile_object = profile
            creator_form.save()
            return redirect('home')
            
        context = {
            'profile_form': profile_form,
            'brand_form': creator_form,
        }
        
        return render(request, self.template_name, context)

    
class CreatorListView(View):
    
    template_name = 'creators_list.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        categories = request.GET.getlist('categories')
        followers = request.GET.get('followers')
        platforms = request.GET.getlist('platforms')

        creators = User.objects.filter(is_brand=False, is_staff=False)

        if search_query:
            creators = creators.filter(
                Q(profile__full_name__icontains=search_query) |
                Q(profile__creator_profile__niche__name__icontains=search_query) |
                Q(profile__creator_profile__platform__name__icontains=search_query)
            ).distinct()

        if categories:
            creators = creators.filter(profile__creator_profile__niche__name__in=categories).distinct()

        if followers:
            if followers == '0-50K':
                creators = creators.filter(profile__creator_profile__follower_count__lte=50)
            elif followers == '50K-100K':
                creators = creators.filter(profile__creator_profile__follower_count__gt=50, profile__creator_profile__follower_count__lte=100)
            elif followers == '100K-500K':
                creators = creators.filter(profile__creator_profile__follower_count__gt=100, profile__creator_profile__follower_count__lte=500)
            elif followers == '500K+':
                creators = creators.filter(profile__creator_profile__follower_count__gt=500)

        if platforms:
            creators = creators.filter(profile__creator_profile__platform__name__in=platforms).distinct()

        all_categories = Niche.objects.all()
        all_platforms = Platform.objects.all()

        context = {
            'creators': creators,
            'search_query': search_query,
            'selected_categories': categories,
            'selected_followers': followers,
            'selected_platforms': platforms,
            'all_categories': all_categories,
            'all_platforms': all_platforms,
        }
        
        return render(request, self.template_name, context)
    
    
class CreatorDetailView(View):
    
    template_name = 'creator_detail.html'
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        qs = User.objects.get(id=id)
        
        context = {
            'creator':qs
        }
        
        return render(request, self.template_name, context)