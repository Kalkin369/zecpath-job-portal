import json
import logging
from datetime import timedelta

import razorpay
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from core.models import BillingHistory, PaymentTransaction, UserSubscription
from core.services.logging_service import LoggingService
from core.tasks import (
    send_payment_failed_email_task,
    send_payment_success_email_task,
    send_refund_processed_email_task
)

logger = logging.getLogger(__name__)


class PaymentGatewayService:

    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def create_order(self, amount, currency="INR"):

        order_data = {
            "amount": int(amount * 100),
            "currency": currency,
            "payment_capture": 1,
        }

        order = self.client.order.create(data=order_data)

        return order

    def verify_signature(
        self, razorpay_order_id, razorpay_payment_id, razorpay_signature
    ):

        data = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        try:

            self.client.utility.verify_payment_signature(data)

            return True

        except razorpay.errors.SignatureVerificationError:

            return False

    def capture_payment(self, payment_id, amount):

        return self.client.payment.capture(payment_id, int(amount * 100))

    def refund_payment(self, payment_id, amount):

        refund = self.client.payment.refund(payment_id, {"amount": int(amount * 100)})

        return refund

    def fetch_payment(self, payment_id):

        return self.client.payment.fetch(payment_id)

    def create_payment_order(self, employer, subscription_id):
        try:
            subscription = UserSubscription.objects.select_related("plan").get(
                id=subscription_id, employer=employer
            )

        except UserSubscription.DoesNotExist:
            raise ValidationError({"subscription_id": ["Subscription not found."]})

        order = self.create_order(amount=subscription.plan.price)

        payment = PaymentTransaction.objects.create(
            subscription=subscription,
            amount=subscription.plan.price,
            transaction_id=order["id"],
            gateway="razorpay",
            gateway_order_id=order["id"],
            status="pending",
        )

        logger.info(
            "Payment order created. Order ID: %s,Employer ID: %s",
            order["id"],
            employer.id,
        )

        return {"payment": payment, "order": order}

    @transaction.atomic
    def verify_payment(
        self, razorpay_order_id, razorpay_payment_id, razorpay_signature
    ):

        payment = PaymentTransaction.objects.select_related("subscription").get(
            gateway_order_id=razorpay_order_id
        )

        # If webhook has already captured the payment,
        # just store the missing verification details.
        if payment.captured:

            payment.verified = True
            payment.payment_signature = razorpay_signature

            if not payment.gateway_payment_id:
                payment.gateway_payment_id = razorpay_payment_id

            payment.save(
                update_fields=["verified", "payment_signature", "gateway_payment_id"]
            )

            logger.info(
                "Payment already captured via webhook. Verification details updated. Order ID: %s",
                razorpay_order_id,
            )

            return {"success": True, "message": "Payment already captured."}

        is_verified = self.verify_signature(
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )

        if not is_verified:

            logger.warning(
                "Payment signature verification failed. Order ID: %s", razorpay_order_id
            )

            payment.status = "failed"

            payment.save(update_fields=["status"])

            return {"success": False, "message": "Signature verification failed."}

        payment.gateway_payment_id = razorpay_payment_id
        payment.payment_signature = razorpay_signature
        payment.verified = True
        payment.transaction_id = razorpay_payment_id

        payment.save()

        logger.info(
            "Payment verified successfully. Payment ID: %s", razorpay_payment_id
        )

        return {
            "success": True,
            "message": "Payment verified successfully. Waiting for webhook confirmation.",
        }

    def process_webhook(self, payload, signature):

        payload = payload.decode("utf-8")

        try:
            self.client.utility.verify_webhook_signature(
                payload, signature, settings.RAZORPAY_WEBHOOK_SECRET
            )
        except razorpay.errors.SignatureVerificationError:

            logger.warning("Invalid Razorpay webhook signature received.")

            return {"success": False, "message": "Invalid webhook signature."}

        try:

            event = json.loads(payload)
            event_name = event["event"]

            logger.info("Received Razorpay webhook: %s", event_name)

            if event_name == "payment.captured":
                return self.handle_payment_captured(event)

            elif event_name == "payment.failed":
                return self.handle_payment_failed(event)

            elif event_name == "refund.created":
                return self.handle_refund_created(event)

            elif event_name == "refund.processed":
                return self.handle_refund_processed(event)

            return {"success": True, "message": f"{event_name} ignored."}

        except Exception:
            logger.exception("webhook processing failed")
            raise

    @transaction.atomic
    def handle_payment_captured(self, event):

        payment_data = event["payload"]["payment"]["entity"]

        payment_id = payment_data["id"]

        order_id = payment_data["order_id"]

        payment = (
            PaymentTransaction.objects.select_related(
                "subscription", "subscription__plan", "subscription__employer"
            )
            .filter(gateway_order_id=order_id)
            .first()
        )

        if not payment:

            logger.warning(
                "Payment transaction not found for gateway payment ID: %s", payment_id
            )

            return {"success": False, "message": "Payment transaction not found."}

        if payment.captured:

            logger.info(
                "Duplicate payment.captured webhook ignored. Payment ID:%s",
                payment.gateway_payment_id,
            )

            return {"success": True, "message": "Payment already processed."}

        payment.gateway_payment_id = payment_id
        payment.status = "success"
        payment.captured = True

        payment.save(update_fields=["gateway_payment_id", "status", "captured"])

        subscription = payment.subscription

        subscription.start_date = timezone.now().date()

        subscription.end_date = subscription.start_date + timedelta(
            days=subscription.plan.duration_days
        )

        subscription.is_active = True

        subscription.save(update_fields=["start_date", "end_date", "is_active"])

        BillingHistory.objects.get_or_create(
            employer=subscription.employer,
            payment=payment,
            defaults={"invoice_number": f"INV-{payment.id}"},
        )

        send_payment_success_email_task.delay(payment.id)

        LoggingService().create_audit_log(
            user=payment.subscription.employer.user,
            action="PAYMENT_SUCCESS",
            entity_type="Payment Transaction",
            entity_id=payment.id,
        )

        logger.info(
            "Payment captured successfully. Payment ID: %s", payment.gateway_payment_id
        )

        return {"success": True, "message": "Payment captured successfully."}

    @transaction.atomic
    def handle_payment_failed(self, event):

        payment_data = event["payload"]["payment"]["entity"]

        payment_id = payment_data["id"]

        order_id = payment_data["order_id"]

        payment = PaymentTransaction.objects.filter(gateway_order_id=order_id).first()

        if not payment:

            logger.warning(
                "Payment transaction not found.Gateway Payment ID: %s", payment_id
            )

            return {"success": False, "message": "Payment transaction not found."}

        payment.gateway_payment_id = payment_id

        payment.status = "failed"

        payment.save(update_fields=["gateway_payment_id", "status"])

        send_payment_failed_email_task.delay(payment.id)

        LoggingService().create_audit_log(
            user=payment.subscription.employer.user,
            action="PAYMENT_FAILED",
            entity_type="Payment Transaction",
            entity_id=payment.id,
        )

        logger.warning("Payment failed. Payment ID: %s", payment.gateway_payment_id)

        return {"success": True, "message": "Payment marked as failed."}

    @transaction.atomic
    def handle_refund_created(self, event):

        refund_data = event["payload"]["refund"]["entity"]

        payment_id = refund_data["payment_id"]

        payment = PaymentTransaction.objects.filter(
            gateway_payment_id=payment_id
        ).first()

        if not payment:

            logger.warning(
                "Payment transaction not found. Gateway Payment ID: %s", payment_id
            )

            return {"success": False, "message": "Payment transaction not found."}

        payment.status = "refunded"

        payment.save(update_fields=["status"])

        LoggingService().create_audit_log(
            user=payment.subscription.employer.user,
            action="REFUND_INITIATED",
            entity_type="Payment Transaction",
            entity_id=payment.id,
        )

        logger.info("Refund initiated. Payment ID: %s", payment.gateway_payment_id)

        return {"success": True, "message": "Refund initiated."}

    @transaction.atomic
    def handle_refund_processed(self, event):

        refund_data = event["payload"]["refund"]["entity"]

        payment_id = refund_data["payment_id"]

        payment = PaymentTransaction.objects.filter(
            gateway_payment_id=payment_id
        ).first()

        if not payment:

            logger.warning(
                "Payment transaction not found,Gateway Payment ID: %s", payment_id
            )

            return {"success": False, "message": "Payment transaction not found."}

        payment.status = "refunded"

        payment.save(update_fields=["status"])

        send_refund_processed_email_task.delay(payment.id)

        LoggingService().create_audit_log(
            user=payment.subscription.employer.user,
            action="REFUND_PROCESSED",
            entity_type="Payment Transaction",
            entity_id=payment.id,
        )

        logger.info(
            "Refund processed successfully. Payment ID: %s", payment.gateway_payment_id
        )

        return {"success": True, "message": "Refund processed successfully."}

    def get_payment_history(self, employer):

        payments = (
            PaymentTransaction.objects.select_related(
                "subscription", "subscription__plan"
            )
            .filter(subscription__employer=employer)
            .order_by("-created_at")
        )

        return payments

    def get_payment_detail(self, employer, payment_id):
        try:
            return PaymentTransaction.objects.select_related(
                "subscription", "subscription__plan", "subscription__employer"
            ).get(id=payment_id, subscription__employer=employer)
        except PaymentTransaction.DoesNotExist:
            raise ValidationError({"payment_id": ["Payment not found."]})

    @transaction.atomic
    def process_refund(self, employer, payment_id, amount):

        try:

            payment = PaymentTransaction.objects.select_related("subscription").get(
                id=payment_id, subscription__employer=employer
            )

        except PaymentTransaction.DoesNotExist:

            raise ValidationError({"payment_id": ["Payment not found."]})

        if payment.status != "success":

            raise ValidationError(
                {"payment": ["Only successful payments can be refunded."]}
            )

        refund = self.refund_payment(payment.gateway_payment_id, amount)

        payment.status = "refund_pending"

        payment.save(update_fields=["status"])

        logger.info(
            "Refund initiated by employer. Payment ID: %s", payment.gateway_payment_id
        )

        return refund
