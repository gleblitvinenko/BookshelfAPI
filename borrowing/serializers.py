from datetime import date

from rest_framework import serializers

from book.models import Book
from book.serializers import BookSerializer
from borrowing.models import Borrowing, Payment


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "book")


class BorrowingDetailSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class CreateBorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = ["book", "expected_return_date"]

    def create(self, validated_data):
        # Add the borrower (current authenticated user) to the validated data
        borrower = self.context["request"].user
        validated_data["borrower"] = borrower

        return super().create(validated_data)


class ReturnBorrowSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField(default=date.today, read_only=True)

    class Meta:
        model = Borrowing
        fields = ["actual_return_date"]

    def update(self, instance, validated_data):
        # Set the actual_return_date to the current date
        instance.actual_return_date = date.today()
        instance.save()
        return instance


class PaymentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("id", "status", "type", "money_to_pay")


class PaymentDetailSerializer(serializers.ModelSerializer):
    borrowing = BorrowingSerializer

    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing", "session_url", "session_id", "money_to_pay")
