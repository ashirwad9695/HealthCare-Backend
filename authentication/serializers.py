from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user public profile."""
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Requires: name, email, password.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        style={'input_type': 'password'},
        help_text="Password must be at least 6 characters."
    )

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty or whitespace.")
        return value.strip()

    def validate_email(self, value):
        normalized = value.strip().lower()
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return normalized

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Accepts: email, password.
    Returns: user object upon validation.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password', '')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(username=email, password=password)
        if not user:
            # Check if user exists to provide helpful error
            try:
                existing = User.objects.get(email__iexact=email)
                if not existing.check_password(password):
                    raise serializers.ValidationError("Invalid email or password.")
                if not existing.is_active:
                    raise serializers.ValidationError("User account is inactive.")
                user = existing
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")

        attrs['user'] = user
        return attrs
