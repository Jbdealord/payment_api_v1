from django.db.models.signals import post_save

from django.dispatch import receiver

from payment_api_v1.models import Payment
from payment_api_v1.tasks import process_payment


@receiver(post_save, sender=Payment, dispatch_uid='process_payment')
def process_payment_signal(sender, instance, created, **kwargs):
    """
    We want to catch the moment, when a `Payment` instance has just created. Processing
    of this payment will be scheduled for background execution.
    """

    if not created:
        return
    process_payment.delay(instance.id)
