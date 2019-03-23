from django.apps import AppConfig


class PaymentAPIv1AppConfig(AppConfig):
    name = 'payment_api_v1'

    def ready(self):
        import payment_api_v1.signals
