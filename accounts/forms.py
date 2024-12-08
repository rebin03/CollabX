from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import BrandProfile, CreatorProfile, Profile, User


class BrandSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'phone']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')

        if commit:
            user.save()
            
        return user
            

class CreatorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
        
        
class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'profile_picture', 'contact_detail', 'address' ]
        

class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = ['niche', 'platform', 'engagement_rate']
        
        widgets = {
            'niche': forms.CheckboxSelectMultiple(),
            'platform': forms.CheckboxSelectMultiple(),
        }
        
class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        fields = ['brand_name', 'website', 'brand_type', 'brand_industry']


