from django.contrib import admin
from accounts.models import BrandIndustry, BrandType, Niche, Platform, Profile

# Register your models here.

admin.site.register(Niche)
admin.site.register(Platform)
admin.site.register(BrandType)
admin.site.register(BrandIndustry)
admin.site.register(Profile)