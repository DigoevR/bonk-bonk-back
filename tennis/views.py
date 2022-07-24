from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from custom_auth.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from custom_auth.models import User
from tennis.serializers import MatchSerializer

class CurrentUserView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class MatchCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchSerializer
    def perform_create(self, serializer):
        serializer.save(requesting_player=self.request.user)