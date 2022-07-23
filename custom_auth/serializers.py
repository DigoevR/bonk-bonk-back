from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'paternal_name', 'email', 'elo']
        read_only_fields = ['elo']