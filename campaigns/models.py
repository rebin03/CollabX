from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone

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
        ('pending', 'Pending'),
        ('closed', 'Closed'),
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
    submitted_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='unpaid')


class DismissedNotification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    dismissed_at = models.DateTimeField(auto_now_add=True)

class EscrowTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    proposal = models.OneToOneField('Proposal', on_delete=models.CASCADE, related_name='escrow_transaction')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"EscrowTransaction for {self.proposal} - {self.status}"

class Rating(models.Model):
    proposal = models.OneToOneField('Proposal', on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating for {self.proposal} - {self.rating}"