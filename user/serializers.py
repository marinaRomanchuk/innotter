from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "role",
            "image_s3_path",
            "title",
            "is_blocked",
        )


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, attrs: dict) -> dict:
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "User with the same email already exists."}
            )
        return attrs

    def create(self, validated_data: dict) -> User:
        user = User.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user
