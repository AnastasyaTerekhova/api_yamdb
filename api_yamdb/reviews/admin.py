from django.contrib import admin

from reviews.models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date',)
    search_fields = ('author',)
    list_filter = ('score',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date',)
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'
