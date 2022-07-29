from rest_framework import serializers, validators

from custom_auth.validators import max_image_size_validator
from .models import User
from django.contrib.auth.password_validation import validate_password
from sorl.thumbnail import get_thumbnail as sorl_get_thumbnail
from sorl.thumbnail import delete as sorl_delete

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=(validate_password,))
    thumbnail = serializers.SerializerMethodField()
    photo = serializers.ImageField(write_only=True, validators=(max_image_size_validator,), required=False)

    def get_thumbnail(self, instance):
        if instance.photo:
            return sorl_get_thumbnail(instance.photo, '124x124', quality=99, crop='center').url

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
        photo = validated_data.get('photo')
        if photo:
            sorl_delete(user.photo)
        return super().update(user, validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'paternal_name', 'email', 'elo', 'password', 'thumbnail', 'photo')
        read_only_fields = ('elo', 'id', 'thumbnail')
        write_only_fields = ('password','photo')


class UsernameValidationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40, validators=(validators.UniqueValidator(User.objects.all(), message='Username already exists'),))
