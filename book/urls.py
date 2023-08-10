from django.urls import path, include
from rest_framework import routers

from book.views import BookViewSet

router = routers.DefaultRouter()
router.register("", viewset=BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "book"
