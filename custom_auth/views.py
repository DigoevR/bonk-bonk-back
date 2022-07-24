from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterUserSerializer, UsernameValidationSerializer
from .permissions import UnauthenticatedOnlyPermission

class LoginView(KnoxLoginView):
    authentication_classes = (BasicAuthentication,)

class SignupView(CreateAPIView):
    permission_classes = (UnauthenticatedOnlyPermission,)
    serializer_class = RegisterUserSerializer

class CheckUsernameView(APIView):
    """Validate username field"""
    def post(self, request):
        serializer = UsernameValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
