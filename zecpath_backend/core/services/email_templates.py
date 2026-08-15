def application_status_template(application):

    return (
        f"Hello "
        f"{application.candidate.user.full_name},\n\n"
        f"Your application for "
        f"{application.job.title} "
        f"is now "
        f"{application.status}.\n\n"
        f"Thank you."
    )


def payment_success_template(payment):

    return (
        f"Hello {payment.subscription.employer.user.full_name},\n\n"
        f"Your payment of ₹{payment.amount} "
        f"for the {payment.subscription.plan.name} plan "
        f"was successful.\n\n"
        f"Transaction ID: {payment.gateway_payment_id}\n\n"
        f"Thank you."
    )


def payment_failed_template(payment):

    return (
        f"Hello {payment.subscription.employer.user.full_name},\n\n"
        f"Your payment for the "
        f"{payment.subscription.plan.name} plan "
        f"could not be completed.\n\n"
        f"Please try again."
    )


def refund_processed_template(payment):

    return (
        f"Hello {payment.subscription.employer.user.full_name},\n\n"
        f"Your refund for payment "
        f"{payment.gateway_payment_id} "
        f"has been processed successfully."
    )
