from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from books.choices import StatusChoices
from books.models import Book, Genre, Author, Publisher, BookLoan, Review, Fine
from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer, GenreSerializer, AuthorSerializer, PublisherSerializer, \
    BookLoanSerializer, ReviewSerializer, FineUpdateSerializer, FineListSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)


class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)


class BookLoanListView(ListCreateAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return BookLoan.objects.filter(user_id=self.request.user.id)

        return BookLoan.objects.all()


class BookLoanDetailView(RetrieveUpdateAPIView):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_update(self, serializer: BookLoanSerializer):
        if serializer.validated_data['status'] == StatusChoices.RETURNED.value:
            serializer.save(actual_return_date=timezone.now().date())


class FineListView(ListAPIView):
    serializer_class = FineListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Fine.objects.filter(loan__reader_id=self.request.user.id)

        return Fine.objects.all()


class FineUpdateView(UpdateAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineUpdateSerializer
    permission_classes = (IsAdminUser,)
