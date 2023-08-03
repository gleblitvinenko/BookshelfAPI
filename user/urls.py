from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user.views import RegisterView, MyProfileView

urlpatterns = [
    path("", RegisterView.as_view(), name="user-registration"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MyProfileView.as_view(), name="user-me"),

]

appname = "user"
