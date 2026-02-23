from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(phone, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        FARMER = 'farmer', 'Farmer'        # Rents tractors
        OWNER  = 'owner',  'Owner'         # Lists tractors for rent
        DEALER = 'dealer', 'Dealer'        # Sells tractors
        ADMIN  = 'admin',  'Admin'

    # Core identity
    name     = models.CharField(max_length=150)
    phone    = models.CharField(max_length=15, unique=True)
    email    = models.EmailField(blank=True, null=True)
    role     = models.CharField(max_length=10, choices=Role.choices, default=Role.FARMER)

    # Profile
    profile_photo = models.ImageField(upload_to='users/photos/', blank=True, null=True)
    location      = models.CharField(max_length=255, blank=True)
    state         = models.CharField(max_length=100, blank=True)
    district      = models.CharField(max_length=100, blank=True)
    pincode       = models.CharField(max_length=10, blank=True)

    # Verification
    verified        = models.BooleanField(default=False)
    aadhaar_number  = models.CharField(max_length=12, blank=True)
    otp             = models.CharField(max_length=6, blank=True)   # temp OTP store
    otp_expiry      = models.DateTimeField(null=True, blank=True)

    # Django internals
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'User'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone}) — {self.role}"
