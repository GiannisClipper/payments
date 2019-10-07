from apps.renderers import GenericJSONRenderer


class UserJSONRenderer(GenericJSONRenderer):
    data_namespace = 'user'
