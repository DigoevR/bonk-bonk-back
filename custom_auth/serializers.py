from rest_framework import serializers, validators
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=(validate_password,))

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, user, validated_data):
        password = validated_data.get('password')
        if password:
            del validated_data['password']
            user.set_password(password)
        return super().update(user, validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'paternal_name', 'email', 'elo', 'password')
        read_only_fields = ('elo', 'id')
        write_only_fields = ('password',)


class UsernameValidationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40, validators=(validators.UniqueValidator(User.objects.all(), message='Username already exists'),))
