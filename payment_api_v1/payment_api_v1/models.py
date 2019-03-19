from django.db import models

from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Balance(models.Model):

    money = MoneyField(
        max_digits=8,  # 999,999,99
        decimal_places=2
    )
    account = models.ForeignKey('Account', null=False, blank=False, on_delete=models.CASCADE)


class Account(models.Model):

    email = models.EmailField(null=False, blank=False)

    def create_balance(self, currency_code: str) -> Balance:
        """
        Creates new balance with given currency for current account

        :param currency_code: currency code
        :return: newly created balance
        """
        return Balance.objects.create(account=self, money=Money(0, currency_code))

