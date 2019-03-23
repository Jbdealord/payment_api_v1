from decimal import Decimal
from unittest import mock

from django.test import TransactionTestCase

from payment_api_v1.models import Account, Payment, Money
from payment_api_v1.tasks import process_payment


class PaymentTestCase(TransactionTestCase):

    def setUp(self):
        self.account_from = Account.objects.create(email='test@example.com')
        self.account_from.create_balance('RUB')
        self.balance_from = self.account_from.create_balance('PHP')
        self.balance_from.money = Money(1000, 'PHP')
        self.balance_from.save()

        self.account_to = Account.objects.create(email='test@example.com')
        self.balance_to = self.account_to.create_balance('PHP')
        self.balance_to.money = Money(500, 'PHP')
        self.balance_to.save()

    def test_make_payment_same_currency_enough_money_mock_processing(self):
        with mock.patch('payment_api_v1.tasks.process_payment.delay') as process_payment_mock:
            payment = Payment.objects.create(
                balance_from=self.balance_from,
                balance_to=self.balance_to,
                money=Money(555.55, 'PHP')
            )
            process_payment_mock.assert_called_once_with(payment.id)
        self.assertEqual(payment.status, Payment.STATUS.pending)
        self.assertEqual(self.balance_from.money.amount, Decimal(1000))
        self.assertEqual(self.balance_to.money.amount, Decimal(500))

    def test_make_payment_same_currency_enough_money_processed(self):
        with mock.patch('payment_api_v1.tasks.process_payment.delay'):
            payment = Payment.objects.create(
                balance_from=self.balance_from,
                balance_to=self.balance_to,
                money=Money(555.55, 'PHP')
            )

        process_payment(payment.id)

        payment.refresh_from_db()
        self.balance_from.refresh_from_db()
        self.balance_to.refresh_from_db()

        self.assertEqual(payment.status, Payment.STATUS.success)
        self.assertEqual(self.balance_from.money.amount, Decimal('444.45'))
        self.assertEqual(self.balance_to.money.amount, Decimal('1055.55'))

    def test_make_payment_same_currency_not_enough_money_processed(self):
        with mock.patch('payment_api_v1.tasks.process_payment.delay'):
            payment = Payment.objects.create(
                balance_from=self.balance_from,
                balance_to=self.balance_to,
                money=Money(1555.55, 'PHP')
            )

        process_payment(payment.id)

        payment.refresh_from_db()
        self.balance_from.refresh_from_db()
        self.balance_to.refresh_from_db()

        self.assertEqual(payment.status, Payment.STATUS.not_enough_money)
        self.assertEqual(self.balance_from.money.amount, Decimal(1000))
        self.assertEqual(self.balance_to.money.amount, Decimal(500))
