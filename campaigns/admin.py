from django.contrib import admin
from campaigns.models import Audience, ContentType

# Register your models here.

admin.site.register(ContentType)
admin.site.register(Audience)