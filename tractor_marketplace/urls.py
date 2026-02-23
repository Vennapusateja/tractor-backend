from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/users/',    include('users.urls')),
    path('api/tractors/', include('listings.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/equipment/',include('equipment.urls')),
    path('api/reviews/',  include('reviews.urls')),
    path('api/payments/', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
