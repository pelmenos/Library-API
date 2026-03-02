from books.models import Review, Author
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from datetime import date
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from books.models import Book, BookLoan, Fine, Genre, Publisher
from books.choices import StatusChoices
from books.consts import FINE_PER_DAY
from books.tasks import create_fines

User = get_user_model()


class BookReviewApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email="test@test.com", password="pass", first_name="N", last_name="L")
        self.genre = Genre.objects.create(name="Fiction")
        self.pub = Publisher.objects.create(name="O'Reilly")
        self.author = Author.objects.create(first_name='Aleksandr', last_name='Pushkin')
        self.book = Book.objects.create(
            title="Python Pro", genre=self.genre, publisher=self.pub,
            isbn="111-222", quantity=5
        )
        self.client.force_authenticate(user=self.user)

    def test_2_get_books(self):
        """2. GET /api/books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_3_create_book(self):
        """3. POST /api/books"""
        url = reverse('book-list')
        data = {
            "title": "New Book", "genre": self.genre.id, "publisher": self.pub.id,
            "isbn": "333-444", "quantity": 10, 'authors': [self.author.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_4_delete_book(self):
        """4. DELETE /api/books/{id}"""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_10_get_reviews(self):
        """10. GET /api/books/reviews"""
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_11_create_review(self):
        """11. POST /api/books/reviews"""
        url = reverse('review-list')
        data = {
            "book": self.book.id, "reader": self.user.id,
            "rating": 5, "comment": "Great!", "date": date.today()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_12_delete_review(self):
        """12. DELETE /api/post/reviews/{id}"""
        review = Review.objects.create(
            book=self.book, reader=self.user, rating=4, comment="Ok", date=date.today()
        )
        # Обратите внимание на путь в вашем условии: /api/post/reviews/
        # Если роутер стандартный, будет 'review-detail'
        url = reverse('review-detail', args=[review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LoanFineApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email="lib@test.com", password="pass")
        self.genre = Genre.objects.create(name="History")
        self.pub = Publisher.objects.create(name="Classic")
        self.book = Book.objects.create(title="History 101", genre=self.genre, publisher=self.pub, isbn="555", quantity=2)
        self.client.force_authenticate(user=self.user)

    def test_8_create_loan(self):
        """8. POST /api/books/loans"""
        url = reverse('bookloan-list')
        data = {
            "book": self.book.id, "reader": self.user.id,
            "loan_date": date.today(), "return_date": date.today() + timedelta(days=7),
            "status": StatusChoices.ISSUED.value
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_9_update_loan(self):
        """9. PUT /api/books/loans/{id}"""
        loan = BookLoan.objects.create(
            book=self.book, reader=self.user,
            loan_date=date.today(), return_date=date.today(), status="active"
        )
        url = reverse('bookloan-detail', args=[loan.id])
        data = {
            "book": self.book.id, "reader": self.user.id,
            "loan_date": loan.loan_date, "return_date": loan.return_date,
            "status": StatusChoices.RETURNED.value, "actual_return_date": date.today()
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_13_get_fines(self):
        """13. GET /api/books/fines"""
        url = reverse('fine-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_14_update_fine(self):
        """14. PUT /api/books/fines/{id}"""
        loan = BookLoan.objects.create(
            book=self.book, reader=self.user,
            loan_date=date.today(), return_date=date.today(), status="overdue"
        )
        fine = Fine.objects.create(loan=loan, amount=100, due_date=date.today())
        due_date = date.today() + timedelta(days=7)
        url = reverse('fine-detail', args=[fine.id])
        data = {"due_date": due_date}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fine.refresh_from_db()
        self.assertEqual(fine.due_date, due_date)


class FineServiceTests(TestCase):
    def setUp(self):
        # Создаем необходимые зависимости
        self.user = User.objects.create_user(email="test@test.com", password="pass")
        self.genre = Genre.objects.create(name="Classic")
        self.pub = Publisher.objects.create(name="Test Pub")
        self.book = Book.objects.create(
            title="Test Book", genre=self.genre, publisher=self.pub,
            isbn="999", quantity=5
        )

    def test_create_fines_logic(self):
        """Проверка, что функция создает штраф для просроченной аренды"""

        # 1. Создаем просроченную аренду (вчерашняя дата возврата)
        yesterday = timezone.now().date() - timedelta(days=1)
        loan = BookLoan.objects.create(
            book=self.book,
            reader=self.user,
            loan_date=yesterday - timedelta(days=7),
            return_date=yesterday,
            status='active'  # Изначально статус активен
        )

        # 2. Вызываем тестируемую функцию
        create_fines()

        # 3. Проверяем изменения в базе данных
        loan.refresh_from_db()

        # Проверка 1: Статус аренды сменился на 'expired'
        self.assertEqual(loan.status, StatusChoices.EXPIRED.value)

        # Проверка 2: Объект штрафа (Fine) был создан
        fine_exists = Fine.objects.filter(loan=loan).exists()
        self.assertTrue(fine_exists)

        # Проверка 3: Сумма штрафа равна FINE_PER_DAY
        fine = Fine.objects.get(loan=loan)
        self.assertEqual(fine.amount, FINE_PER_DAY)