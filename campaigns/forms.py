from django import forms
from campaigns.models import Campaign, ContentType, Audience



class CampaignForm(forms.ModelForm):
    
    content_types = forms.ModelMultipleChoiceField(
        queryset=ContentType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    audience_preferences = forms.ModelMultipleChoiceField(
        queryset=Audience.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'picture', 'budget', 'content_types', 'audience_preferences', 'requirements', 'region']
        
    
    def clean_content_types(self):
        
        content_types = self.cleaned_data.get('content_types')
        
        if not content_types:
            raise forms.ValidationError("You must select at least one content type.")
        return content_types

    def clean_audience_preferences(self):
        
        audience_preferences = self.cleaned_data.get('audience_preferences')
       
        if not audience_preferences:
            raise forms.ValidationError("You must select at least one audience preference.")
        return audience_preferences
