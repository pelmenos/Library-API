from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import BookViewSet, AuthorViewSet, GenreViewSet, PublisherViewSet, BookLoanListView, \
    BookLoanDetailView, FineListView, FineUpdateView, ReviewViewSet

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"publishers", PublisherViewSet, basename="publisher")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
    path("loans", BookLoanListView.as_view(), name="bookloan-list"),
    path("loans/<int:pk>", BookLoanDetailView.as_view(), name="bookloan-detail"),
    path("fines", FineListView.as_view(), name="fine-list"),
    path("fines/<int:pk>", FineUpdateView.as_view(), name="fine-detail"),
]
