from django.db import models
from core.models.user_subscription import UserSubscription

class PaymentTransaction(models.Model):

    STATUS_CHOICES = [

        ('pending','Pending'),

        ('success','Success'),

        ('failed','Failed')
]

    subscription = models.ForeignKey(UserSubscription,on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10,decimal_places=2)

    transaction_id = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)