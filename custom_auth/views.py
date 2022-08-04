from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from .serializers import UserSerializer, UsernameValidationSerializer
from .permissions import UnauthenticatedOnlyPermission

class LoginView(KnoxLoginView):
    authentication_classes = (BasicAuthentication, TokenAuthentication)

class SignupView(CreateAPIView):
    permission_classes = (UnauthenticatedOnlyPermission,)
    serializer_class = UserSerializer

class CheckUsernameView(APIView):
    """Validate username field"""
    def post(self, request):
        serializer = UsernameValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
