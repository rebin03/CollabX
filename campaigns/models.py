from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


class ContentType(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name


class Audience(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Campaign(BaseModel):
    brand = models.ForeignKey('accounts.BrandProfile', on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField()
    picture = models.ImageField(upload_to='campaign_images', null=True, blank=True)
    budget = models.FloatField()
    content_types = models.ManyToManyField(ContentType)
    audience_preferences = models.ManyToManyField(Audience)
    requirements = models.TextField()
    region = models.CharField(max_length=100)
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('close', 'Closed'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    
class Proposal(BaseModel):
    campaign_object = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='proposals')
    creator_object = models.ForeignKey('accounts.CreatorProfile', on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    is_interested = models.BooleanField(default=False)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('working', 'Working'),
        ('completed', 'Completed'),
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_report = models.FileField(upload_to='campaign_reports', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
