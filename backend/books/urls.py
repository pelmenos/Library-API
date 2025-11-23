from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import BookViewSet, AuthorViewSet, GenreViewSet, PublisherViewSet, BookLoanListView, \
    BookLoanDetailView, FineListView, FineUpdateView

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"publishers", PublisherViewSet, basename="publisher")
router.register(r"", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
    path("loans", BookLoanListView.as_view()),
    path("loans/<int:pk>", BookLoanDetailView.as_view()),
    path("fines", FineListView.as_view()),
    path("fines/<int:pk>", FineUpdateView.as_view()),
]
