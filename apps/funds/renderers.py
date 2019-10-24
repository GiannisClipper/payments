from core.renderers import GenericJSONRenderer, Generic2JSONRenderer


class FundJSONRenderer(GenericJSONRenderer):
    data_namespace = 'fund'


class Fund2JSONRenderer(Generic2JSONRenderer):
    data_namespace = 'fund'
