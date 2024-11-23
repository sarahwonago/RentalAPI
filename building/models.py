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

    class Meta:
        unique_together = ["name", "landlord"] # ensure unique buildings per landlord

    def __str__(self):
        return f"{self.name}|{self.address}- {self.landlord}"


class House(models.Model):
    """
    Model representing a House.
    """

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(
        max_length=255,
        help_text="The house name/number"
    )
    building = models.ForeignKey(
        Building,
        related_name="houses",
        on_delete=models.CASCADE,
        help_text="The Building of the House"
    )
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    default_due_day = models.PositiveIntegerField(
        default=10,
        help_text="The default day of the month when rent is due"
    )
    is_occupied = models.BooleanField(default=False)

    class Meta:
        unique_together = ["name", "building"]


    def __str__(self):
        return f"{self.name} in {self.building}"