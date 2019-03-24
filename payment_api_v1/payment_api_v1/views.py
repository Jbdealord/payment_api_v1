from rest_framework import mixins, viewsets

from payment_api_v1.models import Account, Balance, Payment

from payment_api_v1.serializers.account import AccountDetailSerializer, AccountListSerializer
from payment_api_v1.serializers.balance import BalanceDetailSerializer
from payment_api_v1.serializers.payment import PaymentDetailSerializer, PaymentListSerializer


class AccountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    # TODO (dmitry): filter for active
    queryset = Account.objects.all()

    def get_serializer_class(self):
        return self.detail and AccountDetailSerializer or \
               not self.detail and AccountListSerializer


class BalanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    # TODO (dmitry): filter only active balances for active accounts
    queryset = Balance.objects.all()

    def get_serializer_class(self):
        return BalanceDetailSerializer


class PaymentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Payment.objects.all()

    def get_serializer_class(self):
        return self.detail and PaymentDetailSerializer or \
               not self.detail and PaymentListSerializer
