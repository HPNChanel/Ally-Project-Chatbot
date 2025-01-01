from django.urls import path
from .views import ChatHistoryAPI, LoginAPI, RegisterAPI, UserProfileAPI, UserSettingsAPI, AnalyticsAPI, DownloadChatHistoryAPI, ChangePasswordAPI, UpdateUserAPI, DeleteAccountAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', UserProfileAPI.as_view(), name='user_profile'),
    path('chats/', ChatHistoryAPI.as_view(), name='chat_history'),
    path('settings/', UserSettingsAPI.as_view(), name='user_settings'),
    path('analytics/', AnalyticsAPI.as_view(), name='analytics'),
    path('download/', DownloadChatHistoryAPI.as_view(), name='download_chat_history'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('update-profile/', UpdateUserAPI.as_view(), name='update_profile'),
    path('delete-account/', DeleteAccountAPI.as_view(), name='delete_account'),
]
