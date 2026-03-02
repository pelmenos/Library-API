from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from books.choices import StatusChoices
from books.models import Book, Genre, Author, Publisher, BookLoan, Review, Fine
from books.serializers import BookSerializer, GenreSerializer, AuthorSerializer, PublisherSerializer, \
    BookLoanSerializer, ReviewSerializer, FineUpdateSerializer, FineListSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminUser,)


class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminUser,)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminUser,)


class BookLoanListView(ListCreateAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return BookLoan.objects.filter(user_id=self.request.user.id)

        return BookLoan.objects.all()


class BookLoanDetailView(RetrieveUpdateAPIView):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    permission_classes = (IsAdminUser,)

    def perform_update(self, serializer: BookLoanSerializer):
        if serializer.validated_data['status'] == StatusChoices.RETURNED.value:
            serializer.save(actual_return_date=timezone.now().date())


class FineListView(ListAPIView):
    serializer_class = FineListSerializer
    permission_classes = (IsAdminUser,)
    queryset = Fine.objects.all()


class FineUpdateView(UpdateAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineUpdateSerializer
    permission_classes = (IsAdminUser,)
