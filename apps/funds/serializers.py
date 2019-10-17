from rest_framework import serializers

from django.db import models

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Fund  #, error_messages


class UserSerializerField(serializers.RelatedField):

    def get_queryset(self):
        return get_user_model().objects.all()

    def to_representation(self, instance):
        return {'id': instance.pk, 'username': instance.username}

    def to_internal_value(self, data):
        return get_object_or_404(get_user_model(), pk=data)


class FundSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of Fund objects.'''

    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.pk

    user = UserSerializerField()

    url = serializers.HyperlinkedIdentityField(
        view_name='funds:by-id',
        lookup_field='id',
        read_only=True,
    )

    class Meta:
        model = Fund
        fields = ('id', 'user', 'code', 'name', 'url')

        # extra_kwargs = error_messages

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

        return None