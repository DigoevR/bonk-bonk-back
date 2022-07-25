

from django.urls import path
from . import views as dv

urlpatterns = [
    path('user/', dv.CurrentUserView.as_view(), name='current_user'),
    path('user/<int:pk>/', dv.UserDetailView.as_view(), name='user_detail'),
    path('users/', dv.UserListView.as_view(), name='user_list'),

    path('match/', dv.MatchCreateView.as_view(), name='match_create'),
    path('match/<int:pk>/', dv.MatchDetailConfirmRejectView.as_view(), name='match_detail_confirm')
]
