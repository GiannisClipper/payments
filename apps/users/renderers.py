from core.renderers import GenericJSONRenderer


class UserJSONRenderer(GenericJSONRenderer):
    data_namespace = 'user'


class UsersJSONRenderer(GenericJSONRenderer):
    data_namespace = 'users'
