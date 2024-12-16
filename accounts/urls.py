from django.urls import path
from accounts import views

urlpatterns = [
    path('brand/signup/', views.BrandSignUpView.as_view(), name='brand-signup'),
    path('creator/signup/', views.CreatorSignUpView.as_view(), name='creator-signup'),
    path('brand/profile/add/', views.BrandProfileCreateView.as_view(), name='create-brand-profile'),
    path('creator/profile/add/', views.CreatorProfileCreateView.as_view(), name='create-creator-profile'),
    path('verify/email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('signin/', views.SignInView.as_view(), name='signin'),
]
