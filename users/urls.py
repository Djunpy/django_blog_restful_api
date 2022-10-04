from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterViewAPI.as_view(), name='register'),
    path('login/', views.UserLoginViewAPI.as_view(), name='login'),
    path('change-password/',
         views.UserChangePasswordViewAPI.as_view(), name='change-password'),
    path('reset-password/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

]
