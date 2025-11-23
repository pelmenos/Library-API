from django.contrib import admin

from books.models import Genre, Publisher, Book, BookLoan, Fine, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'website']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'publisher', 'publication_year', 'isbn', 'quantity']
    list_filter = ['genre', 'publisher']


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'loan_date', 'return_date', 'status']
    list_filter = ['status', 'loan_date']


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'due_date']
    list_filter = ['due_date']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'rating', 'date']
    list_filter = ['rating', 'date']
