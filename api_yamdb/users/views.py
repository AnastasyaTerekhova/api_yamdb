import re
import uuid
from http import HTTPStatus

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import UserModel
from users.permissions import IsAdmin
from users.serializers import (ConfirmationCodeSerializer, SignupSerializer,
                               UserSerializer, UsersMeSerializer)


class SignupView(APIView):
    """Класс для регистрации пользователей."""

    @staticmethod
    def make_confirmation_code(username):
        """Создает код подтверждения для пользователя."""
        name_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, username)
        return str(name_uuid)

    def post(self, request):

        username = request.data.get('username')
        email = request.data.get('email')
        if UserModel.objects.filter(username=username, email=email).exists():
            return Response({'message': 'Пользователь уже зарегистрирован'},
                            status=HTTPStatus.OK)
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=HTTPStatus.BAD_REQUEST)

        confirmation_code = self.make_confirmation_code(username)
        UserModel.objects.create(username=username, email=email,
                                 confirmation_code=confirmation_code)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='example@gmail.com',
            recipient_list=[email],
            fail_silently=True
        )

        return Response(
            {'email': email, 'username': username},
            status=HTTPStatus.OK
        )


class TokenView(APIView):
    """Класс работы с JWT-токеном."""

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            UserModel,
            username=serializer.validated_data['username']
        )
        confirmation_code = request.data.get('confirmation_code')

        refresh_token = RefreshToken.for_user(user)

        response = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }
        if confirmation_code == user.confirmation_code:
            return Response(response, status=HTTPStatus.OK)
        return Response(
            {'error': 'Неверно указан код подтверждения'},
            status=HTTPStatus.BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователями."""

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(
            self.queryset, username=self.kwargs['username'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        pattern = r'^[\w.@+-]+\Z'
        username = request.data.get('username')
        if username is None:
            return Response(
                {'error': 'Имя пользователя не указано'},
                status=HTTPStatus.BAD_REQUEST)
        if not re.match(pattern, username):
            return Response(
                {'error': 'Имя пользователя не соответствует требованиям. '
                 'Имя пользователя должно содержать только буквы, цифры, '
                 'и символы @/./+/-/_'},
                status=HTTPStatus.BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'error': 'Данный метод запросов не поддерживается'},
                        status=HTTPStatus.METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        """Получение или обновление пользователя."""
        user = get_object_or_404(UserModel, username=self.request.user)
        serializer = UsersMeSerializer(self.request.user)

        if request.method == 'PATCH':
            serializer = UsersMeSerializer(user, data=request.data,
                                           partial=True)
            if 'username' in request.data:
                pattern = r'^[\w.@+-]+\Z'
                username = request.data.get('username')
                if not re.match(pattern, username):
                    return Response(
                        {'error': 'Имя пользователя не соответствует '
                         'требованиям. Имя пользователя должно содержать '
                         'только буквы, цифры, и символы @/./+/-/_'},
                        status=HTTPStatus.BAD_REQUEST)
            if not serializer.is_valid():
                return Response(serializer.errors,
                                status=HTTPStatus.BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.data)
