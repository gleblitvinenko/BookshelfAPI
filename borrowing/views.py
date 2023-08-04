from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingListView(generics.ListAPIView):

    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(borrower=user).select_related("borrower", "book")

    def get_object(self):
        return self.request.user


class BorrowingDetailView(generics.RetrieveAPIView):

    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(borrower=user).select_related("borrower", "book")
