

from django.urls import path
from . import views as dv

urlpatterns = [
    path('user/', dv.CurrentUserView.as_view(), name='current_user_detail_update_delete'),
    path('user/<int:pk>/', dv.UserDetailView.as_view(), name='user_detail'),
    path('users/', dv.UserListView.as_view(), name='user_list'),

    path('match/<int:pk>/', dv.MatchDetailConfirmRejectView.as_view(), name='match_detail_confirm_reject'),
    path('matches/', dv.MatchListCreateView.as_view(), name='match_list_create'),
    path('matches/unconfirmed/', dv.MatchUnconfirmedListView.as_view(), name='match_unconfirmed_list'),
]
