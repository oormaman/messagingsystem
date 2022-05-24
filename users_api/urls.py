from django.urls import path

from users_api import views


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
]
