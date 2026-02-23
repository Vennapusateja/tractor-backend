from rest_framework import generics, permissions, filters
from .models import Equipment
from .serializers import EquipmentSerializer


class EquipmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EquipmentSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['name', 'type', 'brand', 'state', 'district']

    def get_queryset(self):
        return Equipment.objects.filter(is_active=True).select_related('owner').prefetch_related('images')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Equipment.objects.filter(is_active=True)
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
