from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView, CreateAPIView, ListCreateAPIView
from custom_auth.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from custom_auth.models import User
from tennis.models import Match
from tennis.serializers import MatchSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request


class CurrentUserView(RetrieveUpdateDestroyAPIView):
    """
    GET shows current user.
    PATCH updates current user (all fields are considered unrequired when updating).
    DELETE deletes current user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    """
    GET shows user with given id.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    """
    GET shows list of all users.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
    

class MatchListCreateView(ListCreateAPIView):
    """
    GET returns all matches for logged in user.
    POST creates an unconfirmed match.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchSerializer

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(Q(requesting_player=user) | Q(confirming_player=user))

    def perform_create(self, serializer):
        serializer.save(requesting_player=self.request.user)    


class MatchDetailConfirmRejectView(RetrieveAPIView):
    """
    Returns details about match via GET, confirms unconfirmed match via POST and rejects unconfirmed match via DELETE.
    Details about unconfirmed matches, that are not created by user or awaiting confirmation by user return 404.
    Trying to confirm or reject a match that you cannot confirm or reject will return 404.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchSerializer

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(Q(is_confirmed=True) | Q(requesting_player=user) | Q(confirming_player=user))

    def post(self, request, pk):
        user = self.request.user
        match = get_object_or_404(Match.objects.filter(is_confirmed=False, confirming_player=user), pk=pk)
        match.confirm()
        return Response(self.serializer_class(match).data)

    def delete(self, request, pk):
        user = self.request.user
        match = get_object_or_404(Match.objects.filter(is_confirmed=False, confirming_player=user), pk=pk)
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatchUnconfirmedListView(ListAPIView):
    """
    Get returns list of matches, that are awaiting confirmation by user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchSerializer
    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(is_confirmed=False, confirming_player=user)


class MatchesWithUserListView(ListAPIView):
    """
    Returns list of matches of current user vs user with given id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchSerializer
    def get_queryset(self):
        user = self.request.user
        other_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Match.objects.filter((Q(requesting_player=user, confirming_player=other_user) | Q(requesting_player=other_user, confirming_player=user)))