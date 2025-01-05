from django.urls import path
from campaigns import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('brand/dashboard/', views.BrandDashboardView.as_view(), name='brand-dashboard'),
    path('creator/dashboard/', views.CreatorDashbaordView.as_view(), name='creator-dashboard'),
    path('campaign/add/', views.CreateCampaignView.as_view(), name='create-campaign'),
    path('campaign/all/', views.CampaignListView.as_view(), name='campaign-list'),
    path('campaign/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaign/edit/<int:pk>/', views.UpdateCampaignView.as_view(), name='edit-campaign'),
    path('campaign/delete/<int:pk>/', views.DeleteCampaignView.as_view(), name='delete-campaign'),
    path('proposal/submit/<int:pk>/', views.SubmitProposalView.as_view(), name='submit-proposal'),
    path('proposal/accept/<int:pk>/', views.AcceptProposalView.as_view(), name='accept-proposal'),
    path('proposal/reject/<int:pk>/', views.RejectProposalView.as_view(), name='reject-proposal'),
    path('pending-proposals/', views.PendingProposalsView.as_view(), name='pending-proposals'),
    path('cancel-proposal/<int:pk>/', views.CancelProposalView.as_view(), name='cancel-proposal'),
    path('payment/callback/', views.PaymentCallbackView.as_view(), name='payment-callback'),
    path('start-working/<int:pk>/', views.StartWorkingView.as_view(), name='start-working'),
]
