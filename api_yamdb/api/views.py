from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from reviews.models import Category, Comment, Genre, Review, Title

from api.filters import TitleFilter
from api.permissions import (IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)


class FatherListCreateDestroy(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin):
    """Родитель для вьюшек жанров и категорий."""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Реализует CRUD для произведений."""

    queryset = Title.objects.select_related()
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(FatherListCreateDestroy):
    """Выводит список жанров, создает и удаляет отдельные жанры."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(FatherListCreateDestroy):
    """Выводит список категорий, создает и удаляет отдельные категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        # Получаем id произведения из эндпоинта
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        # Отбираем только нужные отзывы
        new_queryset = Review.objects.filter(title=self.get_title())
        return new_queryset

    def perform_create(self, serializer):
        # Передаём новые значения полей в save()
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Класс работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        # Получаем id отзыва из эндпоинта
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        # Отбираем только нужные комментарии
        new_queryset = Comment.objects.filter(review=self.get_review())
        return new_queryset

    def perform_create(self, serializer):
        # Передаём новые значения полей в save()
        serializer.save(author=self.request.user, review=self.get_review())
