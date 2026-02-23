from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tractor, TractorImage
from .serializers import TractorSerializer, TractorWriteSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class TractorListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/tractors/          — list all (with filters)
    POST /api/tractors/          — create (owner/dealer only)
    """
    queryset = Tractor.objects.filter(is_active=True).select_related('owner').prefetch_related('images', 'reviews')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['brand', 'model_name', 'state', 'district', 'location']
    ordering_fields = ['rent_price_per_hour', 'hp', 'year', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TractorWriteSerializer
        return TractorSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        # Filter by query params
        state    = self.request.query_params.get('state')
        district = self.request.query_params.get('district')
        hp_min   = self.request.query_params.get('hp_min')
        hp_max   = self.request.query_params.get('hp_max')
        for_rent = self.request.query_params.get('for_rent')
        for_sale = self.request.query_params.get('for_sale')

        if state:    qs = qs.filter(state__icontains=state)
        if district: qs = qs.filter(district__icontains=district)
        if hp_min:   qs = qs.filter(hp__gte=hp_min)
        if hp_max:   qs = qs.filter(hp__lte=hp_max)
        if for_rent == 'true': qs = qs.exclude(rent_price_per_hour=None, rent_price_per_acre=None)
        if for_sale == 'true': qs = qs.exclude(sell_price=None)
        return qs


class TractorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/tractors/<pk>/"""
    queryset = Tractor.objects.filter(is_active=True)
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return TractorWriteSerializer
        return TractorSerializer

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class MyTractorsView(generics.ListAPIView):
    """GET /api/tractors/mine/  — logged in owner sees their listings"""
    serializer_class = TractorSerializer

    def get_queryset(self):
        return Tractor.objects.filter(owner=self.request.user).prefetch_related('images', 'reviews')


class DeleteTractorImageView(APIView):
    """DELETE /api/tractors/images/<pk>/"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            img = TractorImage.objects.get(pk=pk, tractor__owner=request.user)
        except TractorImage.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        img.image.delete(save=False)
        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
