from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[0][1]['fields'] = ('username', 'password', 'elo')
    fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'paternal_name', 'email')
    list_display = ('username', 'elo', 'first_name', 'last_name', 'paternal_name', 'email', 'is_staff')
admin.site.register(User, CustomUserAdmin)