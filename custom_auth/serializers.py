from rest_framework import serializers, validators
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'paternal_name', 'email', 'elo')
        read_only_fields = ('elo', 'id')


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=(validate_password,))
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password1": "Password fields didn't match."})
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data['password1']
        del validated_data['password1']
        del validated_data['password2']
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'paternal_name', 'email', 'elo', 'password1', 'password2')
        read_only_fields = ('elo', 'id')


class UsernameValidationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40, validators=(validators.UniqueValidator(User.objects.all(), message='Username already exists'),))
