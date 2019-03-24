from urllib.parse import urljoin

from djmoney.money import Money

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from payment_api_v1.models import Account


class AccountAPITestCase(APITestCase):

    def setUp(self):
        self.account1 = Account.objects.create(email='first@example.com')
        self.account2 = Account.objects.create(email='second@example.com')
        self.account3 = Account.objects.create(email='third@example.com')

        self.accounts = [
            self.account1,
            self.account2,
            self.account3
        ]

        balance_usd = self.account2.create_balance('USD')
        balance_usd.money = Money(500, 'USD')
        balance_usd.save()

        balance_php = self.account2.create_balance('PHP')
        balance_php.money = Money(1000, 'PHP')
        balance_php.save()

    def test_get_account_list(self):
        response = self.client.get(reverse('account-list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertListEqual(
            response.data['results'],
            [
                {
                    'url': urljoin(
                        'http://testserver/',
                        reverse('account-detail', kwargs={'pk': page.pk})
                    )
                } for page in self.accounts
            ]
        )

    def test_get_account_detail(self):
        response = self.client.get(reverse('account-detail', kwargs={'pk': self.account2.pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'email': 'second@example.com',
                'balances': [
                    {
                        'id': 1,
                        'amount': '500.00 USD',
                        'currency': 'USD'
                    },
                    {
                        'id': 2,
                        'amount': '1000.00 PHP',
                        'currency': 'PHP'
                    }
                ]
            }
        )
