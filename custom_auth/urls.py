from django.urls import path
from knox import views as knox_views
from . import views as dv
app_name = 'custom_auth'
urlpatterns = [
     path('login/', dv.LoginView.as_view(), name='knox_login'),
     path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
     path('sign-up/', dv.SignupView.as_view(), name='signup'),
     path('check-username/', dv.CheckUsernameView.as_view(), name='check-username')
     
]