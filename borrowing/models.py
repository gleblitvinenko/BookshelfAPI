from _decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    book = models.ForeignKey(
        Book, related_name="book_borrowing", on_delete=models.CASCADE
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrower",
        on_delete=models.CASCADE,
    )

    def validate_future_date(self, value):
        if value < timezone.now().date():
            raise ValidationError("Date must be in the future.")

    def clean(self):
        self.validate_future_date(self.borrow_date)
        self.validate_future_date(self.expected_return_date)

    def __str__(self):
        return f"{self.borrower} borrowed {self.book} on {self.borrow_date}"


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(max_length=50, choices=StatusChoices.choices)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(
        Borrowing, related_name="borrowing", on_delete=models.CASCADE
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.borrowing.actual_return_date and self.borrowing:
            days_borrowed = (
                self.borrowing.actual_return_date - self.borrowing.borrow_date
            ).days
            money_to_pay = Decimal(days_borrowed) * self.borrowing.book.daily_fee
            self.money_to_pay = money_to_pay

        super().save(*args, **kwargs)
