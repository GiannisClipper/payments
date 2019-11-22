from rest_framework import serializers

from django.shortcuts import get_object_or_404

from users.serializers import UserSerializerField
from funds.serializers import FundSerializerField

from .models import Genre  # , error_messages


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of Genre objects.'''

    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.pk

    user = UserSerializerField()

    fund = FundSerializerField(allow_null=True, default=None)

    url = serializers.HyperlinkedIdentityField(
        view_name='genres:by-id',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Genre
        fields = ('id', 'user', 'code', 'name', 'is_incoming', 'fund', 'url')

        # extra_kwargs = error_messages

    # def validate(self, data):
    #     if data.get('fund', None) and data['fund'].user.pk != data['user'].pk:
    #         raise serializers.ValidationError({'fund': 'Not a valid fund.'})

    #     return data

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
