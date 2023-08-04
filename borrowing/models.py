from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from book.models import Book


class Borrowing(models.Model):

    def validate_future_date(self, value):
        if value < timezone.now().date():
            raise ValidationError("Date must be in the future.")

    def validate_actual_return_date(self, value):
        if value is not None and value < self.borrow_date:
            raise ValidationError("Actual return date cannot be earlier than the borrow date.")

    borrow_date = models.DateField(validators=[validate_future_date])
    expected_return_date = models.DateField(validators=[validate_future_date])
    actual_return_date = models.DateField(null=True, blank=True, validators=[validate_actual_return_date])

    book = models.ForeignKey(
        Book, related_name="book_borrowing", on_delete=models.CASCADE
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="borrower",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.borrower} borrowed {self.book} on {self.borrow_date}"
