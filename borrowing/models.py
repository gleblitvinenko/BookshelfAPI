from datetime import date
from typing import Optional, Type

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

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

    @staticmethod
    def validate_date(
        expected_return_date: date,
        actual_return_date: date,
        error_to_raise: Type[ValidationError],
    ):
        if expected_return_date < date.today():
            raise error_to_raise("Return date must be after borrow date!")

        if actual_return_date and actual_return_date <= date.today():
            raise error_to_raise(
                "Actual return date cannot be less or equal borrow date"
            )

    def clean(self) -> None:
        Borrowing.validate_date(
            self.expected_return_date,
            self.actual_return_date,
            ValidationError,
        )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[list[str]] = None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.borrower} borrowed {self.book} on {self.borrow_date}"
