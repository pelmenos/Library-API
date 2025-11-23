from rest_framework import serializers
from books.models import Book, Author, Genre, Publisher, BookLoan, Review, Fine


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = '__all__'


class FineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'


class FineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ('due_date',)

