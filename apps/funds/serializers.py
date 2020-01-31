from rest_framework import serializers

from django.shortcuts import get_object_or_404

from users.serializers import UserSerializerField

from .models import Fund

from genres.constants import (
    USER_REQUIRED,
    CODE_REQUIRED,
    NAME_REQUIRED,
    CODE_EXISTS,
    NAME_EXISTS,
)


class FundSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of Fund objects.'''

    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.pk

    user = UserSerializerField(
        error_messages={
            'required': USER_REQUIRED,
            'null': USER_REQUIRED,
            'blank': USER_REQUIRED,
        }
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='funds:by-id',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Fund
        fields = ('id', 'user', 'code', 'name', 'url')

        extra_kwargs = {
            'code': {
                'error_messages': {
                    'required': CODE_REQUIRED,
                    'null': CODE_REQUIRED,
                    'blank': CODE_REQUIRED,
                },
            },
            'name': {
                'error_messages': {
                    'required': NAME_REQUIRED,
                    'null': NAME_REQUIRED,
                    'blank': NAME_REQUIRED,
                },
            },
        }

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'code'),
                message=CODE_EXISTS
            ),
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'name'),
                message=NAME_EXISTS
            )
        ]

    def create(self, validated_data):
        return Fund.objects.create(**validated_data)

    def get(self, instance):
        return instance

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def delete(self, instance):
        instance.delete()

        return {}


class FundSerializerField(serializers.RelatedField):

    model = None

    def get_queryset(self):
        return Fund.objects.all()

    def to_representation(self, instance):
        return {'id': instance.pk, 'name': instance.name}

    def to_internal_value(self, data):
        return get_object_or_404(self.get_queryset(), pk=data['id']) if data['id'] else None
