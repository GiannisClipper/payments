from core.renderers import GenericJSONRenderer


class PaymentJSONRenderer(GenericJSONRenderer):
    data_namespace = 'payment'


class PaymentsJSONRenderer(GenericJSONRenderer):
    data_namespace = 'payments'
