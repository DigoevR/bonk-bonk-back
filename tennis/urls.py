

from django.urls import path
from . import views as dv

urlpatterns = [
    path('user/', dv.CurrentUserView.as_view(), name='current_user'),
    path('user/<int:pk>/', dv.UserDetailView.as_view(), name='user_detail'),
    path('users/', dv.UserListView.as_view(), name='user_list'),
]
