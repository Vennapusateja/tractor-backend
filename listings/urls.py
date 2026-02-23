from django.urls import path
from . import views

urlpatterns = [
    path('',             views.TractorListCreateView.as_view(), name='tractor-list'),
    path('mine/',        views.MyTractorsView.as_view(),        name='tractor-mine'),
    path('<int:pk>/',    views.TractorDetailView.as_view(),     name='tractor-detail'),
    path('images/<int:pk>/', views.DeleteTractorImageView.as_view(), name='tractor-image-delete'),
]
