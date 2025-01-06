from django import forms
from campaigns.models import Campaign, ContentType, Audience, Proposal



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


class ReportForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['report_description', 'report_image', 'report_video', 'report_pdf']
        widgets = {
            'report_description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border rounded bg-white focus:ring-2 focus:ring-purple-500 focus:outline-none'}),
            'report_image': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border rounded bg-white focus:ring-2 focus:ring-purple-500 focus:outline-none'}),
            'report_video': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border rounded bg-white focus:ring-2 focus:ring-purple-500 focus:outline-none'}),
            'report_pdf': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border rounded bg-white focus:ring-2 focus:ring-purple-500 focus:outline-none'}),
        }