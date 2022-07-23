from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class UnauthenticatedOnlyPermission(permissions.BasePermission):
    message = "User is already authenticated."
    def has_permission(self, request, view):
        return request.user.is_anonymous