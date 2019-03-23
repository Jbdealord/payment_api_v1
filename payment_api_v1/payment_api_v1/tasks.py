from celery import shared_task

from django.db import transaction

from payment_api_v1.exceptions import NotEnoughMoneyException


@shared_task
def process_payment(payment_id):

    from payment_api_v1.models import Payment

    payment = Payment.objects.get(pk=payment_id)

    try:
        with transaction.atomic():
            payment.balance_from.money -= payment.money
            payment.balance_from.save()

            if payment.balance_from.money.amount < 0:
                raise NotEnoughMoneyException

            payment.balance_to.money += payment.money
            payment.balance_to.save()

            payment.status = Payment.STATUS.success

            payment.save()
    except NotEnoughMoneyException:
        payment.status = Payment.STATUS.not_enough_money
        payment.save()
    except:
        payment.status = Payment.STATUS.system_failure
        payment.save()
