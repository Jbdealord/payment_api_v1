from rest_framework import mixins, viewsets

from payment_api_v1.models import Account
from payment_api_v1.serializers.account import AccountDetailSerializer, AccountListSerializer


class AccountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Account.objects.all()

    def get_serializer_class(self):
        return self.detail and AccountDetailSerializer or \
               not self.detail and AccountListSerializer
