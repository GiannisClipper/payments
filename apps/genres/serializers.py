from rest_framework import serializers

from users.serializers import UserSerializerField
from funds.serializers import FundSerializerField

from .models import Genre  # , error_messages


def validate_fund_user(self): 
    if self.get('fund', None) and self['fund'].user.pk != self['user'].pk:
        raise serializers.ValidationError('Not a proper fund.')


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
        fields = ('id', 'user', 'code', 'name', 'is_income', 'fund', 'url')

        validators = (validate_fund_user,)

        # extra_kwargs = error_messages

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
