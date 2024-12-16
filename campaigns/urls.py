from django.urls import path
from campaigns import views

urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('brand/dashboard/', views.BrandDashboardView.as_view(), name='brand-dashboard'),
    path('campaign/add/', views.CreateCampaignView.as_view(), name='add-campaign')
]
