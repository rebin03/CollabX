from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    
class User(AbstractUser):
    otp = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, unique=True)
    is_brand = models.BooleanField(default=False)
    
    def generate_otp(self):
        
        self.otp = str(randint(10,99)) + str(randint(10,99)) + str(randint(10,99))
        self.save()
        
    @property
    def has_profile(self):
        return hasattr(self, 'profile')


class Profile(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    contact_detail = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name


class Niche(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Platform(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    
class CreatorProfile(BaseModel):
    profile_object = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='creator_profile')
    niche = models.ManyToManyField(Niche)
    platform = models.ManyToManyField(Platform)
    engagement_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    past_collaboration = models.ManyToManyField('campaigns.Campaign')
    

class BrandType(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    
class BrandIndustry(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class BrandProfile(BaseModel):
    profile_object = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='brand_profile')
    brand_name = models.CharField(max_length=50, null=False, blank=False)
    website = models.CharField(max_length=250, null=True, blank=True)
    brand_type = models.ForeignKey(BrandType, on_delete=models.SET_NULL, null=True)
    brand_industry = models.ForeignKey(BrandIndustry, on_delete=models.SET_NULL, null=True)
    campaign_posted = models.ManyToManyField('campaigns.Campaign')