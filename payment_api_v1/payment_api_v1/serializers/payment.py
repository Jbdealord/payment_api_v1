from rest_framework import serializers

from djmoney.money import Money

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


class PaymentCreateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField('payment-detail', read_only=True)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2, write_only=True)

    class Meta:
        model = Payment
        fields = ('balance_from', 'balance_to', 'amount', 'url', )
        extra_kwargs = {
            'balance_from': {'write_only': True},
            'balance_to': {'write_only': True},
        }

    def create(self, validated_data):
        if validated_data['balance_from'].money.currency != validated_data['balance_to'].money.currency:
            raise serializers.ValidationError('Only transactions with same currency are allowed')

        amount = validated_data.pop('amount')
        currency = validated_data['balance_from'].money.currency

        validated_data['money'] = Money(amount, currency.code)

        return super().create(validated_data)
