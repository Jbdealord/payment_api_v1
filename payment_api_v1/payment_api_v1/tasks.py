from celery import shared_task

from django.db import transaction

from payment_api_v1.exceptions import NotEnoughMoneyException, CurrenciesDontMatch


@shared_task
def process_payment(payment_id: int):
    """
    Celery task to process payment. All changes are performed in DB tranasction.
    Transaction is rolled back in case of a problem.

    :param payment_id: id of the `Payment` instance
    """

    from payment_api_v1.models import Payment

    payment = Payment.objects.get(pk=payment_id)

    try:
        if payment.balance_from.money.currency != payment.balance_to.money.currency:
            raise CurrenciesDontMatch

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
    except CurrenciesDontMatch:
        payment.status = Payment.STATUS.currencies_dont_match
        payment.save()
    except:
        payment.status = Payment.STATUS.system_failure
        payment.save()
