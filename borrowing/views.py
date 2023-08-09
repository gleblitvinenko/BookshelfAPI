import asyncio
from datetime import date

from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from book.models import Book
from borrowing.bot import send_notifications_in_group
from borrowing.models import Borrowing, Payment
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    CreateBorrowingSerializer,
    ReturnBorrowSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
)


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related("borrower", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset_ = Borrowing.objects.select_related("borrower", "book")
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id is not None and user.is_staff:
            queryset_ = queryset_.filter(borrower=user_id)

        if user.is_staff is False:
            return queryset_.filter(borrower=user).select_related("borrower", "book")

        if is_active is not None:
            queryset_ = queryset_.filter(actual_return_date__isnull=True)

        return queryset_

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBorrowingSerializer
        return BorrowingSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        book_id = serializer.validated_data.get("book")
        try:
            book = Book.objects.get(pk=book_id.id)
        except Book.DoesNotExist:
            raise ValidationError("The selected book does not exist.")

        book_inventory = book.inventory
        if book_inventory > 0:
            book.inventory -= 1
            book.save()
        else:
            raise ValidationError("No such books left")

        serializer.save(borrower=self.request.user)
        asyncio.run(
            send_notifications_in_group(
                f"✉️ New borrowing\n"
                f"🤠 From {self.request.user.email}\n"
                f"📕 Book: {book_id.title}\n"
                f"⬅️ Expected return date: {serializer.validated_data.get('expected_return_date')}"
            )
        )


class BorrowingDetailView(generics.RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        borrowing_id = self.kwargs.get("id")
        if user.is_staff is False:
            return Borrowing.objects.filter(borrower=user).select_related(
                "borrower", "book"
            )
        return Borrowing.objects.filter(pk=borrowing_id)


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = ReturnBorrowSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_update(self, serializer):
        borrowing = serializer.instance

        if borrowing.borrower != self.request.user:
            raise ValidationError("You are not allowed to return this borrowing.")

        if borrowing.actual_return_date is not None:
            raise ValidationError("This borrowing has already been returned.")

        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.actual_return_date = date.today()
        borrowing.save()

        asyncio.run(
            send_notifications_in_group(
                f"📩 Returned borrowing\n"
                f"🤠 From {self.request.user.email}\n"
                f"📕 Book: {borrowing.book.title}\n"
                f"⬅️ Return date {borrowing.actual_return_date}"
            )
        )


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.select_related("borrowing")
    serializer_class = PaymentListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset_ = Payment.objects.select_related("borrowing")

        if user.is_staff is False:
            queryset_ = queryset_.filter(borrowing__borrower=user).select_related(
                "borrowing"
            )
        return queryset_


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        payment_id = self.kwargs.get("id")

        if user.is_staff is False:
            return Payment.objects.filter(borrowing__borrower=user).select_related(
                "borrowing"
            )

        return Payment.objects.filter(pk=payment_id)
