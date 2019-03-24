from rest_framework import serializers

from payment_api_v1.models import Payment


class PaymentDetailSerializer(serializers.ModelSerializer):

    balance_from = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='balance-detail'
    )
    balance_to = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='balance-detail'
    )
    datetime = serializers.DateTimeField(format='%s')
    amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id', 'balance_from', 'balance_to', 'datetime', 'amount', 'currency', 'status', )

    def get_amount(self, payment):
        return payment.money.amount

    def get_currency(self, payment):
        return payment.money_currency

    def get_status(self, payment):
        return Payment.STATUS[payment.status]


class PaymentListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Payment
        fields = ('url', )
        extra_kwargs = {
            'url': {'view_name': 'payment-detail'}
        }
