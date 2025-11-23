from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator

from books.choices import StatusChoices


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True, validators=[URLValidator()])

    class Meta:
        db_table = 'publishers'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey('books.Genre', on_delete=models.CASCADE)
    publisher = models.ForeignKey('books.Publisher', on_delete=models.CASCADE)
    publication_year = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    authors = models.ManyToManyField('books.Author', related_name='books')

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class BookLoan(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    reader = models.ForeignKey('users.User', on_delete=models.CASCADE)
    loan_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices)

    class Meta:
        db_table = 'book_loans'

    def __str__(self):
        return f"{self.book.title} - {self.reader}"


class Fine(models.Model):
    loan = models.OneToOneField('books.BookLoan', related_name="fine", on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'fines'

    def __str__(self):
        return f"Fine #{self.id} - {self.amount}"


class Review(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    reader = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    date = models.DateField()

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Review for {self.book.title} by {self.reader}"


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'authors'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

