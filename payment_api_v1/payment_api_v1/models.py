from django.db import models
from django.utils.translation import ugettext_lazy as _

from djmoney.models.fields import MoneyField
from djmoney.money import Money

from model_utils import Choices


class Balance(models.Model):

    money = MoneyField(
        max_digits=8,  # 999,999,99
        decimal_places=2
    )
    account = models.ForeignKey('Account', null=False, blank=False, on_delete=models.CASCADE, related_name='balances')

    def __str__(self):
        return f'Balance: ' \
            f'of {self.account} ' \
            f'amount {self.money.amount} ' \
            f'currency {self.money.currency}'

    class Meta:
        ordering = ('id', )


class Account(models.Model):

    email = models.EmailField(null=False, blank=False)

    def create_balance(self, currency_code: str) -> Balance:
        """
        Creates new balance with given currency for current account

        :param currency_code: currency code
        :return: newly created balance
        """
        return Balance.objects.create(account=self, money=Money(0, currency_code))

    def __str__(self):
        return f'Account: {self.email}'

    class Meta:
        ordering = ('email', )


class Payment(models.Model):

    STATUS = Choices(
        (0, 'pending', _('pending')),
        (1, 'success', _('success')),
        (2, 'not_enough_money', _('not_enough_money')),
        (3, 'system_failure', _('system_failure')),
        (4, 'currencies_dont_match', _('currencies_dont_match'))
    )

    balance_from = models.ForeignKey(
        'Balance',
        related_name='payments_from',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    balance_to = models.ForeignKey(
        'Balance',
        related_name='payments_to',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.pending
    )
    money = MoneyField(
        max_digits=8,  # 999,999,99
        decimal_places=2
    )

    def __str__(self):
        return f'' \
            f'Payment [{self.STATUS[self.status]}]: ' \
            f'from {self.balance_from} ' \
            f'to {self.balance_to} ' \
            f'amount {self.money.amount} ' \
            f'currency {self.money.currency}'

    class Meta:
        ordering = ('-datetime', )
