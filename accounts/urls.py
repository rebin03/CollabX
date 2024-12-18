from django.urls import path
from accounts import views

urlpatterns = [
    path('brand/signup/', views.BrandSignUpView.as_view(), name='brand-signup'),
    path('creator/signup/', views.CreatorSignUpView.as_view(), name='creator-signup'),
    path('brand/profile/add/', views.BrandProfileCreateView.as_view(), name='create-brand-profile'),
    path('creator/profile/add/', views.CreatorProfileCreateView.as_view(), name='create-creator-profile'),
    path('verify/email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('creator/all/', views.CreatorListView.as_view(), name='creator-list'),
    path('creator/<int:pk>/', views.CreatorDetailView.as_view(), name='creator-detail'),
    path('campaign/all/', views.CampaignListView.as_view(), name='campaign-list'),
]