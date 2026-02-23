from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['id', 'booking', 'amount', 'status', 'razorpay_order_id', 'created_at']
    list_filter   = ['status']
    search_fields = ['booking__farmer__name', 'razorpay_order_id', 'razorpay_payment_id']
    raw_id_fields = ['booking']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
