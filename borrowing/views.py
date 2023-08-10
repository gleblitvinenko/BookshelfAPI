from typing import Type, Optional

from django.db.models import QuerySet
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnBookSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Borrowing]:
        """
        Return borrowings only for current user.
        Filtering if borrowing has not returned yet.
        Admin can see all users borrowings, and filtering borrowing by user id.
        """
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = Borrowing.objects.filter(borrower=self.request.user)

        if self.request.user.is_staff:
            if user_id:
                queryset = queryset.filter(borrower_id=user_id)

        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date=None)

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        """Return serializer depending on the action"""
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        if self.action == "return_book":
            return BorrowingReturnBookSerializer

        return self.serializer_class

    def perform_create(self, serializer: Serializer[Borrowing]) -> None:
        """Create borrowing only for current user"""
        serializer.save(borrower=self.request.user)

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="return",
        permission_classes=[permissions.IsAuthenticated],
    )
    def return_book(self, request: Request, pk: Optional[int] = None) -> Response:
        """Endpoint for return book specific borrowing"""
        borrowing = self.get_object()
        book = borrowing.book
        serializer = self.get_serializer(
            borrowing, data=request.data, partial=True, context={"pk": pk}
        )
        serializer.is_valid(raise_exception=True)
        book.inventory += 1
        book.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# asyncio.run(
#      send_notifications_in_group(
#          f"📩 Returned borrowing\n"
#          f"🤠 From {self.request.user.email}\n"
#          f"📕 Book: {borrowing.book.title}\n"
#          f"⬅️ Return date {borrowing.actual_return_date}"
#      )
#  )
