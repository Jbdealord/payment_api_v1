from rest_framework import mixins, viewsets

from payment_api_v1.models import Account, Balance, Payment

from payment_api_v1.serializers.account import (
    AccountDetailSerializer,
    AccountListSerializer
)
from payment_api_v1.serializers.balance import BalanceDetailSerializer
from payment_api_v1.serializers.payment import (
    PaymentDetailSerializer,
    PaymentListSerializer,
    PaymentCreateSerializer
)


class AccountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
    Return information about given Account

    list:
    Present a list of URLs, pointing to detail view of each Account in the system
    """

    # TODO (dmitry): filter for active
    queryset = Account.objects.all()

    def get_serializer_class(self):
        return self.detail and AccountDetailSerializer or \
               not self.detail and AccountListSerializer


class BalanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
    Return information about given Balance
    """

    # TODO (dmitry): filter only active balances for active accounts
    queryset = Balance.objects.all()

    def get_serializer_class(self):
        return BalanceDetailSerializer


class PaymentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    retrieve:
    Return information about given Payment

    list:
    Gives a list of URLs, pointing to detail view of each Payment

    create:
    Creates a new Payment and schedules it for further processing. Note: only same currency
    transaction are allowed for now.
    """

    queryset = Payment.objects.all()

    def get_serializer_class(self):
        return self.detail and PaymentDetailSerializer or \
               not self.detail and self.request and self.request.method == 'POST' and PaymentCreateSerializer or \
               not self.detail and PaymentListSerializer
