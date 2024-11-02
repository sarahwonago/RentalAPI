import uuid

from django.db import models
from django.contrib.auth import get_user_model

from tenant.models import Tenant

User = get_user_model()


class Notification(models.Model):
    """
    Model representing a penalty applied to a monthly rent if due date is passed.
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(default=False)

    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
        )

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient}"

    