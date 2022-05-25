from django.urls import path, include
from users_api import views
from .views import RegisterView, LoginView, LogoutView,MessageView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('message', MessageView.as_view()),
]
