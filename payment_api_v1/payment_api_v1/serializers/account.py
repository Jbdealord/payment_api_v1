from rest_framework import serializers

from payment_api_v1.models import Account
from payment_api_v1.serializers.balance import BalanceDetailSerializer


class AccountDetailSerializer(serializers.ModelSerializer):

    balances = BalanceDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('email', 'balances', )


class AccountListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = ('url', )
        extra_kwargs = {
            'url': {'view_name': 'account-detail'}
        }
