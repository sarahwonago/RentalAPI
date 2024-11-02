import uuid

from django.db import models

from tenant.models import Tenant

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
        Tenant, 
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
    
    



