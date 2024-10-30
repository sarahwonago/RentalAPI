import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Building(models.Model):
    """
    A model for representing buildings.
    """

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(
        max_length=255,
        help_text="The Building name"
    )
    address = models.CharField(
        max_length=255,
        help_text="The Building Address"
    )
    landlord = models.ForeignKey(
        User,
        related_name="buildings",
        on_delete=models.CASCADE,
        help_text="The Building Owner",
        limit_choices_to={'role':'landlord'}
    )
    house_numbers = models.PositiveIntegerField(
        help_text="Number of houses in the building"
    )


    def __str__(self):
        return f"{self.name}|{self.address}- {self.landlord}"
