from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password_confirm = attrs.get('password_confirm')
    #
    #     if password != password_confirm:
    #         raise AuthenticationFailed('Invalid password')
    #
    #     return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=2)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
