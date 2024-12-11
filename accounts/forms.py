from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import BrandIndustry, BrandProfile, BrandType, CreatorProfile, Profile, User


class BrandSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'phone', 'is_brand']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        user.is_brand = True

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
    
    brand_type = forms.ModelChoiceField(
        queryset=BrandType.objects.all(),
        required=False,
        empty_label="Select brand type",
        widget=forms.Select(attrs={
            "class": "mt-1 p-2 border block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500",
            "id": "brand-type",
        })
    )
    brand_industry = forms.ModelChoiceField(
        queryset=BrandIndustry.objects.all(),
        required=False,
        empty_label="Select industry",
        widget=forms.Select(attrs={
            "class": "mt-1 p-2 border block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500",
            "id": "industry",
        })
    )
    
    class Meta:
        model = BrandProfile
        fields = ['brand_name', 'website', 'brand_type', 'brand_industry']


