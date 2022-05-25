from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users_api import views


router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserViewSet)
router.register('chat',views.UserChatViewSet)
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
]