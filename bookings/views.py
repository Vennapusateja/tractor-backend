from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer, BookingStatusUpdateSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/bookings/   — farmer sees their bookings
    POST /api/bookings/   — farmer creates booking
    """
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        user = self.request.user
        # Farmers see their own bookings; owners see bookings for their tractors
        if user.role in ('owner', 'dealer'):
            return Booking.objects.filter(tractor__owner=user).select_related('tractor', 'farmer')
        return Booking.objects.filter(farmer=user).select_related('tractor', 'farmer')

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class BookingDetailView(generics.RetrieveAPIView):
    """GET /api/bookings/<pk>/"""
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(
            farmer=user
        ) | Booking.objects.filter(tractor__owner=user)


class BookingStatusView(APIView):
    """PATCH /api/bookings/<pk>/status/  — owner confirms/cancels/completes"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, tractor__owner=request.user)
        except Booking.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = BookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(BookingSerializer(booking).data)


class CancelBookingView(APIView):
    """POST /api/bookings/<pk>/cancel/  — farmer cancels their booking"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, farmer=request.user)
        except Booking.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        if booking.status not in ('pending', 'confirmed'):
            return Response({'detail': 'Cannot cancel this booking.'}, status=400)

        booking.status = 'cancelled'
        booking.save()
        return Response({'detail': 'Booking cancelled.'})
