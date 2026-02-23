from django.urls import path
from . import views

urlpatterns = [
    path('',             views.PaymentListView.as_view(),    name='payment-list'),
    path('<int:pk>/',    views.PaymentDetailView.as_view(),  name='payment-detail'),
    path('initiate/',    views.InitiatePaymentView.as_view(),name='payment-initiate'),
    path('verify/',      views.VerifyPaymentView.as_view(),  name='payment-verify'),
]
