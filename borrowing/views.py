from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingListView(generics.ListAPIView):

    queryset = Borrowing.objects.select_related("borrower", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class BorrowingDetailView(generics.RetrieveAPIView):

    queryset = Borrowing.objects.select_related("borrower", "book")
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
