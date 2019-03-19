from django.test import TestCase

from djmoney.money import Money, Currency

from payment_api_v1.models import Account, Balance


class AccountTestCase(TestCase):

    def setUp(self):
        self.account = Account.objects.create(email='test@example.com')

    def test_create_balance_currency_exists(self):
        balance = self.account.create_balance('RUB')

        self.assertIsInstance(balance, Balance)
        self.assertIsInstance(balance.account, Account)
        self.assertIsInstance(balance.money, Money)

        self.assertEqual(balance.account.id, self.account.id)
        self.assertEqual(balance.money, Money(0, 'RUB'))
        self.assertEqual(balance.money.amount, 0)
        self.assertEqual(balance.money.currency.code, 'RUB')
