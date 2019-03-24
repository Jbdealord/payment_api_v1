from decimal import Decimal

from djmoney.money import Money

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from payment_api_v1.models import Account


class BalanceAPITestCase(APITestCase):

    def setUp(self):
        self.account = Account.objects.create(email='tomviolence@example.com')

        self.balance_usd = self.account.create_balance('USD')
        self.balance_usd.money = Money(500, 'USD')
        self.balance_usd.save()

        self.balance_php = self.account.create_balance('PHP')
        self.balance_php.money = Money(1000, 'PHP')
        self.balance_php.save()

    def test_get_account_detail(self):
        response = self.client.get(reverse('balance-detail', kwargs={'pk': self.balance_php.pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'id': self.balance_php.pk,
                'amount': Decimal(1000.00),
                'currency': 'PHP'
            }
        )
