from django.urls import path
from .views import ChatHistoryAPI, LoginAPI, RegisterAPI, UserProfileAPI, UserSettingsAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', UserProfileAPI.as_view(), name='user_profile'),
    path('chats/', ChatHistoryAPI.as_view(), name='chat_history'),
    path('settings/', UserSettingsAPI.as_view(), name='user_settings'),
]
