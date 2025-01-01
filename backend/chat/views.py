from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, ChatHistorySerializer, UserSettingsSerializer, UpdateUserSerializer
from django.contrib.auth import authenticate
from .models import UserProfile, ChatHistory, UserSettings
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.cache import cache
import requests
from django.conf import settings
import csv
from django.http import HttpResponse

class RegisterAPI(APIView):
  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(APIView):
  
  class Meta:
    pass
  
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      tokens = serializer.validated_data
      return Response(
        {
          "message": "Login successful",
          "refresh_token": tokens['refresh'],
          "access_token": tokens['access']
        }  
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)
  
  def put(self, request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryPagination(PageNumberPagination):  #* Inherits from class PageNumberPagination for pagination
  page_size = 20  #* Amounts of message each page
  page_size_query_param = 'page_size'
  max_page_size = 100  #* The maximum in each page

class ChatHistoryAPI(ListAPIView):
  serializer_class = ChatHistorySerializer
  permission_classes = [IsAuthenticated]
  pagination_class = ChatHistoryPagination
  
  def get_queryset(self):
    user = self.request.user
    cache_key = f"chat_history_user_{user.id}"  #* Cache key for each user
    cached_data = cache.get(cache_key)  #* Get data from cache
    
    if cached_data:
      return cached_data  #* Return data(if in cache)
    
    #* Query if it not in cache
    chats = ChatHistory.objects.filter(user=user).order_by('-timestamp')
    cache.set(cache_key, chats, timeout=300)  #* Save to cache in 500secs
    return chats
  
  def post(self, request):
    serializer = ChatHistorySerializer(data=request.data)
    if serializer.is_valid():
      user_message = serializer.save(user=request.user)
    
      ai_url = f"{settings.BASE_URL}/api/ai/gpt4/"
      
      try:
        ai_response = requests.post(
          ai_url,
          json={"message": user_message.message},
          headers={"Authorization": f"Bearer {request.auth.token}"}
        )
        if ai_response.status_code == 200:
          bot_response = ai_response.json().get("response", "AI is not available")
        else:
          bot_response = "AI service returned an error."
      except Exception as e:
        bot_response = "Failed to connect to AI service."
      
      #* Save chatbot's response
      ChatHistory.objects.create(
        user=request.user,
        message=bot_response,
        is_bot=True
      )
      #* Delete cache if it has new data
      cache_key = f"chat_history_user_{request.user.id}"
      cache.delete(cache_key)

      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSettingsAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    serializer = UserSettingsSerializer(settings)
    return Response(serializer.data)
  
  def put(self, request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    serializer = UserSettingsSerializer(settings, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalyticsAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    user = request.user
    
    #* Count the amount of messages
    total_messages = ChatHistory.objects.filter(user=user).count()
    bot_messages = ChatHistory.objects.filter(user=user, is_bot=True).count()
    user_messages = total_messages - bot_messages
    
    return Response({
      "total_messages": total_messages,
      "user_messages": user_messages,
      "bot_messages": bot_messages
    })

class DownloadChatHistoryAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request):
    user = request.user
    chats = ChatHistory.objects.filter(user=user).order_by("timestamp")
    
    #* Create CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chat_history.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Message', 'Is Bot'])
    
    for chat in chats:
      writer.writerow([chat.timestamp, chat.message, chat.is_bot])
    
    return response

class ChangePasswordAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not request.user.check_password(old_password):
      return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.set_password(new_password)
    request.user.save()
    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

class UpdateUserAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def put(self, request):
    serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def delete(self, request):
    user = request.user
    user.delete()
    return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
  
