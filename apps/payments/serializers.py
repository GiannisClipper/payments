from rest_framework import serializers
from django.db import IntegrityError

from users.serializers import UserSerializerField
from funds.serializers import FundSerializerField
from genres.serializers import GenreSerializerField

from .models import Payment  # , error_messages

from payments.constants import (
    USER_REQUIRED,
    DATE_REQUIRED,
    GENRE_REQUIRED,
    FUND_REQUIRED,
    PAYMENT_EXISTS,
    GENRE_INVALID,
    FUND_INVALID,
)


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of Payment objects.'''

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

    genre = GenreSerializerField(
        error_messages={
            'required': GENRE_REQUIRED,
            'null': GENRE_REQUIRED,
            'blank': GENRE_REQUIRED,
        }
    )

    fund = FundSerializerField(
        error_messages={
            'required': FUND_REQUIRED,
            'null': FUND_REQUIRED,
            'blank': FUND_REQUIRED,
        }
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='payments:by-id',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks', 'url'
        )

        extra_kwargs = {
            'date': {
                'error_messages': {
                    'required': DATE_REQUIRED,
                    'null': DATE_REQUIRED,
                    'blank': DATE_REQUIRED,
                },
            },
            'incoming': {'required': False},
            'outgoing': {'required': False},
            'remarks': {'required': False},
        }

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks'),
                message=PAYMENT_EXISTS
            ),
        ]

    def validate(self, data):
        errors = {}

        if data.get('genre', None) and data['genre'].user.pk != data['user'].pk:
            errors['genre'] = GENRE_INVALID

        if data.get('fund', None) and data['fund'].user.pk != data['user'].pk:
            errors['fund'] = FUND_INVALID

        if errors:
            raise IntegrityError(errors)

        return data

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

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
