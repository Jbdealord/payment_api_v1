from rest_framework import serializers

from payment_api_v1.models import Balance


class BalanceDetailSerializer(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = Balance
        fields = ('id', 'amount', 'currency', )

    def get_amount(self, balance):
        return balance.money.amount

    def get_currency(self, balance):
        return balance.money_currency
