from rest_framework import serializers

from api.services.models import Services, ServiceNumber
from api.users.models import User


class ServicesDataTableSerializer(serializers.ModelSerializer):
    flag = serializers.FileField(required=False, allow_null=True, default=None)
    is_active = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Services
        fields = ("id", "name", "flag", "is_active")

    def create(self, validated_data):
        return Services.objects.create(
            **validated_data,
            is_active=True
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if validated_data.get("flag"):
            instance.flag = validated_data.get('flag', instance.flag)
        instance.save()
        return instance


class ServicesNumberSerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(required=True, allow_null=True)
    service_id = serializers.IntegerField(required=True, allow_null=False)
    id = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(required=True, allow_null=False)
    number = serializers.CharField(required=True, allow_null=False)
    is_active = serializers.BooleanField(read_only=True)
    is_paid = serializers.BooleanField()
    country_name = serializers.CharField(read_only=True, source="country.name")
    service_name = serializers.CharField(read_only=True, source="service.name")

    class Meta:
        model = ServiceNumber
        fields = ("id", "price", "number", "is_active","is_paid",  "service_id", "country_id", "country_name", "service_name")

    def create(self, validated_data):
        return ServiceNumber.objects.create(
            **validated_data,
            is_active=True
        )

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.number = validated_data.get('number', instance.number)
        instance.service_id = validated_data.get('service_id', instance.service_id)
        instance.country_id = validated_data.get('country_id', instance.country_id)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()
        return instance


class ServicesNumberHomeSerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(required=True, allow_null=True)
    id = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(required=True, allow_null=False)
    number = serializers.CharField(required=True, allow_null=False)
    service_name = serializers.CharField(read_only=True, source="service.name")
    flag = serializers.FileField(read_only=True, source="service.flag")

    class Meta:
        model = ServiceNumber
        fields = ("id", "price", "number", "country_id", "flag", "service_name")

