from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):

    username = serializers.CharField(
        min_length=3,
        max_length=150,
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )

class LoginUserSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )