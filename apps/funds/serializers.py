from rest_framework import serializers

from django.shortcuts import get_object_or_404

from users.serializers import UserSerializerField

from .models import Fund  # , error_messages


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


class FundSerializerField(serializers.RelatedField):

    model = None

    def get_queryset(self):
        return Fund.objects.all()

    def to_representation(self, instance):
        return {'id': instance.pk, 'name': instance.name}

    def to_internal_value(self, data):
        return get_object_or_404(self.get_queryset(), pk=data['id'])
