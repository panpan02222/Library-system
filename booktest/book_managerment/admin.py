from django.contrib import admin

from django.contrib import admin
from .models import *


class BookModal(admin.StackedInline):
    model = Book


@admin.register(Publish)
class PublishAdmin(admin.ModelAdmin):
    inlines = [BookModal]
    list_display = ('id', 'name', 'city', 'email', 'books')
    fields = ('name', 'city', 'email')
    list_filter = ['city']
    search_fields = ['name', 'city']

    def books(self, obj):
        return [book.title for book in obj.book_set.all()]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'pub_date', "publish_name", "author")
    fields = ('title', 'price', 'pub_date', "authors")
    search_fields = ['title', 'price', 'pub_date']

    def author(self, obj):
        return [author.name for author in obj.authors.all()]

    def publish_name(self, obj):
        return obj.publish.name

    filter_horizontal = ('authors',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'tel', 'addr', 'birthday', 'books')
    fields = ('name', 'age', 'gender', 'tel', 'addr', 'birthday')
    list_filter = ['gender']
    search_fields = ['name', 'age', 'gender', 'tel', 'addr', 'birthday']

    def books(self, obj):
        return [book.title for book in obj.book_set.all()]
