from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import viewsets

from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == "list":
            return (AllowAny(), )
        return (IsAdminUser(), )

