class BasePaymentException(Exception):

    pass


class NotEnoughMoneyException(BasePaymentException):

    pass


class CurrenciesDontMatch(BasePaymentException):

    pass
