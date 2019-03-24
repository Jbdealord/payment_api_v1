from rest_framework import mixins, viewsets

from payment_api_v1.models import Account, Balance
from payment_api_v1.serializers.account import AccountDetailSerializer, AccountListSerializer
from payment_api_v1.serializers.balance import BalanceDetailSerializer


class AccountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Account.objects.all()

    def get_serializer_class(self):
        return self.detail and AccountDetailSerializer or \
               not self.detail and AccountListSerializer


class BalanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Balance.objects.all()

    def get_serializer_class(self):
        return BalanceDetailSerializer
