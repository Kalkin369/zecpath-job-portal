from django.db import models

from core.models.user_subscription import UserSubscription


class PaymentTransaction(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        related_name="payment_transactions"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    gateway = models.CharField(
        max_length=20,
        default="razorpay"
    )

    gateway_order_id = models.CharField(
        max_length=200,
        blank=True
    )

    gateway_payment_id = models.CharField(
        max_length=200,
        blank=True
    )

    payment_signature = models.TextField(
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    verified = models.BooleanField(
        default=False
    )

    captured = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.gateway} - {self.status}"