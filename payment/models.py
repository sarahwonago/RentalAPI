import uuid

from django.db import models

from lease.models import Lease


class MonthlyRent(models.Model):
    """
    Model representing a monthlyrent payment.
    """

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    lease = models.ForeignKey(
        Lease,
        on_delete=models.CASCADE,
        related_name="monthlyrent"
    )
    month = models.PositiveSmallIntegerField() # 1-12 January-December
    year = models.PositiveSmallIntegerField()
    due_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_penalized = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ["lease", "month", "year"]


    def save(self, *args, **kwargs):
        # Update remaining balance based on payments
        self.remaining_balance = self.rent_amount - self.paid_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lease} - {self.month}/{self.year}"



class Payment(models.Model):
    """
    Model for recording payments.
    """

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    lease = models.ForeignKey(
        Lease, 
        on_delete=models.CASCADE, 
        related_name="payments"
        )
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_transaction_id = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        # Update the lease account with this payment amount
        self.lease.account += self.amount
        self.lease.save()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment of {self.amount} on {self.payment_date}"



class Penalty(models.Model):
    """
    Model representing a penalty applied to a monthly rent if due date is passed.
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    monthly_rent = models.OneToOneField(
        MonthlyRent,
        on_delete=models.CASCADE,
        related_name="penalty"
    )

    amount_penalized = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date_penalized = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Penalty for:{self.monthly_rent}"