from django.db import models

from .employer import Employer
from .payment_transaction import PaymentTransaction


class BillingHistory(models.Model):

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    payment = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)

    invoice_number = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
