import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from building.models import House
class Lease(models.Model):
    """
    Model representing a lease.
    """

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    tenant = models.OneToOneField(
        User, 
        related_name="lease",
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'tenant'}
        )
    
    house = models.OneToOneField(
        House,
        related_name="lease",
        on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    account = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"Lease:{self.tenant}"
    