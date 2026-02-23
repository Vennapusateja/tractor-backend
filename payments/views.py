import hmac
import hashlib
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer, InitiatePaymentSerializer, VerifyPaymentSerializer
from bookings.models import Booking


class InitiatePaymentView(APIView):
    """
    POST /api/payments/initiate/
    Body: { "booking_id": 5 }
    Returns Razorpay order details for front-end checkout.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = Booking.objects.get(
                pk=serializer.validated_data['booking_id'],
                farmer=request.user,
                status='confirmed',
            )
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found or not confirmed.'}, status=404)

        if hasattr(booking, 'payment') and booking.payment.status == 'success':
            return Response({'detail': 'Already paid.'}, status=400)

        amount_paise = int(booking.total_price * 100)  # Razorpay uses paise

        # --- Razorpay order creation ---
        # Uncomment when razorpay package is installed:
        #
        # import razorpay
        # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        # rz_order = client.order.create({
        #     'amount': amount_paise,
        #     'currency': 'INR',
        #     'payment_capture': 1,
        # })
        # razorpay_order_id = rz_order['id']

        # Placeholder for development without razorpay package:
        razorpay_order_id = f"order_dev_{booking.pk}"

        payment, _ = Payment.objects.get_or_create(
            booking=booking,
            defaults={'amount': booking.total_price},
        )
        payment.razorpay_order_id = razorpay_order_id
        payment.status = 'pending'
        payment.save()

        return Response({
            'razorpay_order_id': razorpay_order_id,
            'amount': amount_paise,
            'currency': 'INR',
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'booking_id': booking.pk,
        })


class VerifyPaymentView(APIView):
    """
    POST /api/payments/verify/
    Front-end sends back Razorpay callback data; we verify signature and mark paid.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            payment = Payment.objects.get(razorpay_order_id=data['razorpay_order_id'])
        except Payment.DoesNotExist:
            return Response({'detail': 'Payment record not found.'}, status=404)

        # Verify HMAC-SHA256 signature
        body          = f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}"
        expected_sig  = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            body.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Skip signature check in dev when key is empty
        sig_valid = (not settings.RAZORPAY_KEY_SECRET) or (expected_sig == data['razorpay_signature'])

        if sig_valid:
            payment.razorpay_payment_id = data['razorpay_payment_id']
            payment.razorpay_signature  = data['razorpay_signature']
            payment.status              = 'success'
            payment.save()

            # Mark booking as active
            booking = payment.booking
            booking.status = 'active'
            booking.save()

            return Response({'detail': 'Payment verified. Booking is now active.'})
        else:
            payment.status = 'failed'
            payment.failure_reason = 'Signature mismatch'
            payment.save()
            return Response({'detail': 'Invalid payment signature.'}, status=400)


class PaymentListView(generics.ListAPIView):
    """GET /api/payments/  — user sees their payments"""
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(booking__farmer=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(booking__farmer=self.request.user)
