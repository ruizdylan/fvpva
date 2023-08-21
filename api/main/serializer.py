from rest_framework import serializers

from api.users.models import User
from main.models import Countries


class CountriesDataTableSerializer(serializers.ModelSerializer):
    flag = serializers.FileField(required=False, allow_null=True, default=None)
    is_active = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Countries
        fields = ("id", "name", "flag", "is_active", "dialling_code")

    def create(self, validated_data):
        return Countries.objects.create(
            **validated_data,
            is_active=True
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dialling_code = validated_data.get('dialling_code', instance.dialling_code)
        if validated_data.get("flag"):
            instance.flag = validated_data.get('flag', instance.flag)
        instance.save()
        return instance

