from django.urls import path
from users_api import views


urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('createmessage', views.CreateMessageView.as_view()),
    path('deletemessage', views.DeleteMessageView.as_view()),
    path('getmessage', views.GetMessageFromSpecificUserView.as_view()),
    path('getmessages', views.GetAllMessagesFromSpecificUser.as_view()),
    path('getunreadmessages', views.GetAllUnreadMessagesFromSpecificUser.as_view()),
]