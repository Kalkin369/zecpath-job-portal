from django.conf import settings
from django.views.generic import TemplateView


class PaymentTestView(TemplateView):

    template_name = "payment_test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["razorpay_key_id"] = settings.RAZORPAY_KEY_ID

        return context