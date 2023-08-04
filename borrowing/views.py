from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

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

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):

    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(borrower=user).select_related("borrower", "book")

#
# class CreateBorrowingView(generics.CreateAPIView):
#
#     serializer_class = CreateBorrowingSerializer
#     permission_classes = (IsAuthenticated, )
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CreateBorrowingSerializer
#         return BorrowingSerializer
