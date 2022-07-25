from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from custom_auth.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from custom_auth.models import User
from tennis.models import Match
from tennis.serializers import MatchSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


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
