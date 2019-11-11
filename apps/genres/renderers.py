from core.renderers import GenericJSONRenderer


class GenreJSONRenderer(GenericJSONRenderer):
    data_namespace = 'genre'


class GenresJSONRenderer(GenericJSONRenderer):
    data_namespace = 'genres'
