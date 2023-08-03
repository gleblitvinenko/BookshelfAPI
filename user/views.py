from rest_framework import generics

from user.permissions import AllowUnauthenticatedOnly
from user.serializers import UserRegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowUnauthenticatedOnly, )
