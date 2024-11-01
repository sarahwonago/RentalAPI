import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom user model with roles for superadmin, landlord and tenant.

    Additional fields:
        role: role of the user
        phone_number: Phone number of the user.
    """

    LANDLORD = "landlord"
    TENANT = "tenant"
    SUPERADMIN = "superadmin"
    
    ROLE_CHOICES = (
        ("landlord", "landlord"),
        ("tenant", "tenant"),
        ("superadmin", "superadmin") 
    )

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        unique=True
        )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        blank=True,
        null=True,
        help_text="Role either: 'superadmin','landlord' or 'tenant'."
        )

    def __str__(self):
        return f"{self.username}"
    