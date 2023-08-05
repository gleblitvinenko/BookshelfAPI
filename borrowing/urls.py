from django.urls import path

from borrowing.views import BorrowingListView, BorrowingDetailView, BorrowingReturnView

urlpatterns = [
    path("", BorrowingListView.as_view(), name="borrowing-list"),
    path("<int:id>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("<int:id>/return/", BorrowingReturnView.as_view(), name="borrowing-return"),
]

appname = "borrowing"



