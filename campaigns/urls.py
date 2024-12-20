from django.urls import path
from campaigns import views

urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('brand/dashboard/', views.BrandDashboardView.as_view(), name='brand-dashboard'),
    path('creator/dashboard/', views.CreatorDashbaordView.as_view(), name='creator-dashboard'),
    path('campaign/add/', views.CreateCampaignView.as_view(), name='create-campaign'),
    path('campaign/all/', views.CampaignListView.as_view(), name='campaign-list'),
    path('campaign/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
]
