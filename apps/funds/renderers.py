from core.renderers import GenericJSONRenderer


class FundJSONRenderer(GenericJSONRenderer):
    data_namespace = 'fund'


class FundsJSONRenderer(GenericJSONRenderer):
    data_namespace = 'funds'
