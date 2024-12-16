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
    brand = models.ForeignKey('accounts.BrandProfile', on_delete=models.CASCADE, related_name='campaign')
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