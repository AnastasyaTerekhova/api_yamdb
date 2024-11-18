from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserModel
from users.validators import username_validator


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью UserModel."""

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=UserModel.objects.all()),
        ])
    email = serializers.EmailField(
        required=True, validators=[
            UniqueValidator(queryset=UserModel.objects.all())
        ])

    class Meta:
        model = UserModel
        fields = ('username', 'email')
        extra_kwargs = {
            'password': {'required': False},
        }
        validators = [
            username_validator,
        ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью UserModel."""

    class Meta:
        model = UserModel
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью UserModel."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        fields = ('username', 'confirmation_code')


class UsersMeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью UserModel."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = '__all__'
