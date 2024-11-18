from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import UserModel

NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50


class Category(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH, unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска')
    rating = models.IntegerField(default=None, null=True,
                                 verbose_name='Рейтинг произведения')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(limit_value=1,
                                      message='Минимальная оценка: 1'),
                    MaxValueValidator(limit_value=10,
                                      message='Максимальная оценка: 10')],
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True, db_index=True
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # исключим возможность создания более одного отзыва на произведение
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='Unique review constraint'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True, db_index=True
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:20]
