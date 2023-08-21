from rest_framework import serializers

from api.users.models import User


class AuthenticateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.code', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_email_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'role', "is_active", 'is_email_verified')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

    # def get_role(self, obj):
    #     try:
    #         return obj.role.name
    #     except:
    #         return ''


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    role = serializers.StringRelatedField(many=False, read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_email_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', "email", 'role', 'is_active', "is_email_verified"]

    def create(self, validated_data):
        return User.objects.create(
            **validated_data,
            is_active=True,
            is_staff=False,
            is_superuser=False
        )


class SocialAuthenticateSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    backend = serializers.CharField(required=True, allow_blank=False, allow_null=False)

