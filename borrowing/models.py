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
