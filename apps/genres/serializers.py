from rest_framework import serializers
from django.db import IntegrityError

from django.shortcuts import get_object_or_404

from users.serializers import UserSerializerField
from funds.serializers import FundSerializerField

from .models import Genre

from genres.constants import (
    USER_REQUIRED,
    CODE_REQUIRED,
    NAME_REQUIRED,
    CODE_EXISTS,
    NAME_EXISTS,
    FUND_INVALID,
)


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of Genre objects.'''

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

    fund = FundSerializerField(allow_null=True, default=None)

    url = serializers.HyperlinkedIdentityField(
        view_name='genres:by-id',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Genre
        fields = ('id', 'user', 'code', 'name', 'is_incoming', 'fund', 'url')

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

    def validate(self, data):
        if data.get('fund', None) and data['fund'].user.pk != data['user'].pk:
            raise IntegrityError({'fund': FUND_INVALID})

        return data

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def get(self, instance):
        return instance

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def delete(self, instance):
        instance.delete()

        return None


class GenreSerializerField(serializers.RelatedField):

    model = None

    def get_queryset(self):
        return Genre.objects.all()

    def to_representation(self, instance):
        return {'id': instance.pk, 'name': instance.name}

    def to_internal_value(self, data):
        return get_object_or_404(self.get_queryset(), pk=data['id'])
