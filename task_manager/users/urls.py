from django.urls import path

from .views import UsersView, UserCreateView


urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='user_create'),
]
