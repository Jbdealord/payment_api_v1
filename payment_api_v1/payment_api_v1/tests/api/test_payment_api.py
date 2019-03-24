from decimal import Decimal
from unittest import mock
from urllib.parse import urljoin

from djmoney.money import Money

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from payment_api_v1.models import Account, Payment, Balance
from payment_api_v1.tasks import process_payment


class PaymentAPITestCase(APITestCase):

    def setUp(self):
        self.account1 = Account.objects.create(email='first@example.com')
        self.account2 = Account.objects.create(email='second@example.com')
        self.account3 = Account.objects.create(email='third@example.com')

        self.account2_balance_usd = self.account2.create_balance('USD')
        self.account2_balance_usd.money = Money(500, 'USD')
        self.account2_balance_usd.save()

        self.account2_balance_php = self.account2.create_balance('PHP')
        self.account2_balance_php.money = Money(1000, 'PHP')
        self.account2_balance_php.save()

        self.account3_balance_php = self.account3.create_balance('PHP')
        self.account3_balance_php.money = Money(300, 'PHP')
        self.account3_balance_php.save()

        with mock.patch('payment_api_v1.tasks.process_payment.delay'):
            # pending
            self.payment_pending = Payment.objects.create(
                balance_from=self.account2_balance_php,
                balance_to=self.account3_balance_php,
                money=Money(700, 'PHP')
            )

            # success
            self.payment_success = Payment.objects.create(
                balance_from=self.account2_balance_php,
                balance_to=self.account3_balance_php,
                money=Money(700, 'PHP')
            )

            # not enough money
            self.payment_not_enough_money = Payment.objects.create(
                balance_from=self.account2_balance_php,
                balance_to=self.account3_balance_php,
                money=Money(700, 'PHP')
            )

        # no need to process pending - keep it pending!
        process_payment(self.payment_success.id)
        process_payment(self.payment_not_enough_money.id)

        self.payments = [
            self.payment_pending,
            self.payment_success,
            self.payment_not_enough_money
        ]

    def test_get_payment_list(self):
        response = self.client.get(reverse('payment-list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertListEqual(
            response.data['results'],
            [
                {
                    'url': urljoin(
                        'http://testserver/',
                        reverse('payment-detail', kwargs={'pk': payment.pk})
                    )
                } for payment in self.payments
            ]
        )

    def test_get_payment_detail_for_pending(self):
        response = self.client.get(reverse('payment-detail', kwargs={'pk': self.payment_pending.pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'id': self.payment_pending.pk,
                'balance_from': urljoin(
                    'http://testserver/',
                    reverse('balance-detail', kwargs={'pk': self.payment_pending.balance_from.pk})
                ),
                'balance_to': urljoin(
                    'http://testserver/',
                    reverse('balance-detail', kwargs={'pk': self.payment_pending.balance_to.pk})
                ),
                'datetime': self.payment_pending.datetime,
                'amount': Decimal(700),
                'currency': 'PHP',
                'status': 'pending'
            }
        )

    def test_get_payment_detail_for_success(self):
        response = self.client.get(reverse('payment-detail', kwargs={'pk': self.payment_success.pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'id': self.payment_success.pk,
                'balance_from': urljoin(
                    'http://testserver/',
                    reverse('balance-detail', kwargs={'pk': self.payment_success.balance_from.pk})
                ),
                'balance_to': urljoin(
                    'http://testserver/',
                    reverse('balance-detail', kwargs={'pk': self.payment_success.balance_to.pk})
                ),
                'datetime': self.payment_success.datetime,
                'amount': Decimal(700),
                'currency': 'PHP',
                'status': 'success'
            }
        )

    def test_get_payment_detail_for_not_enough_money(self):
        response = self.client.get(
            reverse('payment-detail', kwargs={'pk': self.payment_not_enough_money.pk}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'id': self.payment_not_enough_money.pk,
                'balance_from': urljoin(
                    'http://testserver/',
                    reverse('balance-detail', kwargs={'pk': self.payment_not_enough_money.balance_from.pk})
                ),
                'balance_to': urljoin(
                    'http://testserver/',
                    reverse('balance-detail', kwargs={'pk': self.payment_not_enough_money.balance_to.pk})
                ),
                'datetime': self.payment_not_enough_money.datetime,
                'amount': Decimal(700),
                'currency': 'PHP',
                'status': 'not_enough_money'
            }
        )
