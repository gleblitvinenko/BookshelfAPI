from django.urls import path

from borrowing.views import BorrowingListView, BorrowingDetailView

urlpatterns = [
    path("", BorrowingListView.as_view(), name="borrowing-list"),
    path("<int:id>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
]

appname = "borrowing"



