from rest_framework import serializers

from users.serializers import UserSerializerField
from funds.serializers import FundSerializerField
from genres.serializers import GenreSerializerField

from .models import Payment  # , error_messages


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of Payment objects.'''

    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.pk

    user = UserSerializerField()

    genre = GenreSerializerField()

    fund = FundSerializerField()

    url = serializers.HyperlinkedIdentityField(
        view_name='payments:by-id',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = ('id', 'user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks', 'url')

        extra_kwargs = {
            'incoming': {'required': False},
            'outgoing': {'required': False},
            'remarks': {'required': False}
        } 
        # extra_kwargs = error_messages

    def validate(self, data):
        if data.get('genre', None) and data['genre'].user.pk != data['user'].pk:
            raise serializers.ValidationError({'genre': 'Not a valid genre.'})

        if data.get('fund', None) and data['fund'].user.pk != data['user'].pk:
            raise serializers.ValidationError({'fund': 'Not a valid fund.'})

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