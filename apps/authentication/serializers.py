from rest_framework import serializers, exceptions
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            },
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            }
        }

    def create(self, validated_data):
        data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
            'email': validated_data['email'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'is_active': False  # False to make the user activate its account
        }
        # Check if the emails is not used by another user
        if User.objects.filter(email=data['email']).exists():
            raise exceptions.ValidationError({'email': ['Ya existe un usuario usando este email.']})
        return User.objects.create_user(**data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
