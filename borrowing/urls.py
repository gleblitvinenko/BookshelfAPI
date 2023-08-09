from django.urls import path

from borrowing.views import (
    BorrowingListView,
    BorrowingDetailView,
    BorrowingReturnView,
    PaymentListView,
    PaymentDetailView,
)

urlpatterns = [
    path("", BorrowingListView.as_view(), name="borrowing-list"),
    path("<int:id>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("<int:id>/return/", BorrowingReturnView.as_view(), name="borrowing-return"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/<int:id>/", PaymentDetailView.as_view(), name="payment-detail"),
]

appname = "borrowing"
