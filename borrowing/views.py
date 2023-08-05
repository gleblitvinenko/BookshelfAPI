from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer, CreateBorrowingSerializer


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related("borrower", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(borrower=user).select_related("borrower", "book")

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBorrowingSerializer
        return BorrowingSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        request_data = serializer.validated_data
        book_id = serializer.validated_data.get("book")
        print(book_id)

        try:
            book = Book.objects.get(pk=book_id.id)
            print(book)
        except Book.DoesNotExist:
            raise ValidationError("The selected book does not exist.")

        book_inventory = book.inventory
        if book_inventory > 0:
            book.inventory -= 1
            book.save()
        else:
            raise ValidationError("No such books left")

        serializer.save(borrower=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):

    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(borrower=user).select_related("borrower", "book")
