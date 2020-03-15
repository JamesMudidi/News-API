from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
from rest_framework.response import Response


class RegistrationSerializer(serializers.ModelSerializer):
    # Serialize registration requests and register a new user.

    user_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        error_messages={
            'max_length': 'Password should be not more than {max_length} characters',
            'min_length': 'Password should be not less than {min_length} characters'
        }
    )
    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['user_name', 'email',
                  'password', 'confirmed_password']

    def validate(self, data):
        # Validate data before it gets saved.
        confirmed_password = data.get('confirmed_password')
        try:
            validate_password(data['password'])
        except ValidationError as identifier:
            raise serializers.ValidationError({
                'password': str(identifier).replace(
                    '['', '').replace('']', '')})

        if not self.do_passwords_match(data['password'], confirmed_password):
            raise serializers.ValidationError({
                    'passwords': ('Passwords do not match')
                })
        return data

    def create(self, validated_data):
        # Create a user.
        del validated_data['confirmed_password']
        return User.objects.create_user(**validated_data)

    def do_passwords_match(self, password1, password2):
        # Check if passwords match.
        return password1 == password2


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True,)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user_name = data.get('user_name', None)
        user = authenticate(email=email, password=password, user_name=user_name)
        if user is None:
            raise serializers.ValidationError({
                'error': 'The Username or Password entered is wrong'
            })
        user = {
            'email': user.email,
            'user_name': user.user_name,
            'token': user.token
        }
        return user
