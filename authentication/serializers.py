import jwt
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import authenticate

from user.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        email = validated_data["email"]
        password = validated_data["password"]
        error_msg = "email or password are incorrect"
        try:
            user = User.objects.get(email=email)
            if authenticate(username=email, password=password):
                raise serializers.ValidationError(error_msg)
            validated_data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            "iss": "backend-api",
            "user_id": validated_data["user"].id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TTL),
            "type": 'access'
        }
        access = jwt.encode(payload=access_payload, key=settings.SECRET_KEY)

        refresh_payload = {
            "iss": "backend-api",
            "user_id": validated_data["user"].id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_REFRESH_TTL),
            "type": "refresh"
        }
        refresh = jwt.encode(payload=refresh_payload, key=settings.SECRET_KEY)

        return {
            "access": access,
            "refresh": refresh
        }


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        refresh_token = validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload["type"] != "refresh":
                error_msg = {"refresh_token": "Token type is not refresh!"}
                raise serializers.ValidationError(error_msg)
            validated_data["payload"] = payload
        except jwt.ExpiredSignatureError:
            error_msg = {'refresh_token': 'Refresh token is expired!'}
            raise serializers.ValidationError(error_msg)
        except jwt.InvalidTokenError:
            error_msg = {'refresh_token': 'Refresh token is invalid!'}
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            "iss": "backend-api",
            "user_id": validated_data["payload"]["user_id"],
            "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TTL),
            "type": 'access'
        }
        access = jwt.encode(payload=access_payload, key=settings.SECRET_KEY)

        refresh_payload = {
            "iss": "backend-api",
            "user_id": validated_data["payload"]["user_id"],
            "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_REFRESH_TTL),
            "type": "refresh"
        }
        refresh = jwt.encode(payload=refresh_payload, key=settings.SECRET_KEY)

        return {
            "access": access,
            "refresh": refresh
        }
