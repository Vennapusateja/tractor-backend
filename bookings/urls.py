from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.BookingListCreateView.as_view(), name='booking-list'),
    path('<int:pk>/',           views.BookingDetailView.as_view(),     name='booking-detail'),
    path('<int:pk>/status/',    views.BookingStatusView.as_view(),     name='booking-status'),
    path('<int:pk>/cancel/',    views.CancelBookingView.as_view(),     name='booking-cancel'),
]
