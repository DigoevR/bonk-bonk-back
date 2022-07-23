from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView

from .serializers import RegisterUserSerializer
from .permissions import UnauthenticatedOnlyPermission

class LoginView(KnoxLoginView):
    authentication_classes = (BasicAuthentication,)

class SignupView(CreateAPIView):
    permission_classes = (UnauthenticatedOnlyPermission,)
    serializer_class = RegisterUserSerializer
