from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, ChatHistorySerializer
from django.contrib.auth import authenticate
from .models import UserProfile, ChatHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.cache import cache

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
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']
      user = authenticate(username=username, password=password)
      if user:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
      return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
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
    cache_key = f"chat_history_user()"
  
