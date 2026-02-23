from django.urls import path
from . import views

urlpatterns = [
    path('',          views.EquipmentListCreateView.as_view(), name='equipment-list'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(),     name='equipment-detail'),
]
