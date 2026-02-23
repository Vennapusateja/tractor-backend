from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        tractor_id = self.request.query_params.get('tractor')
        qs = Review.objects.select_related('user')
        if tractor_id:
            qs = qs.filter(tractor_id=tractor_id)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveDestroyAPIView):
    queryset         = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Review.objects.filter(user=self.request.user)
        return Review.objects.all()
