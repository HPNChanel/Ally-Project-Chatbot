from rest_framework import serializers
from .models import CustomUser, UserProfile, ChatHistory
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)  #* `write_only: only write, cannot read`
  
  class Meta:
    model = CustomUser
    fields = ['full_name', 'username', 'email', 'password']
    
  def create(self, validated_data):
    user = CustomUser.objects.create_user(  #* Like CREATE in dtb, instead of using this, we use create through CustomUser base class
      username=validated_data['username'],
      email=validated_data['email'],
      full_name = validated_data['full_name'],
      password=validated_data['password'],
    )
  
    return user

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(required=True)
  password = serializers.CharField(write_only=True, required=True)
  
  def validate(self, data):
    username = data.get("username")
    password = data.get("password")
    
    user = authenticate(username=username, password=password)
    if not user:
      raise serializers.ValidationError("Invalid credentials")
    
    #* Create token
    refresh = RefreshToken.for_user(user)
    return {
      'refresh': str(refresh),
      'access': str(refresh.access_token)
    }

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['avatar', 'bio', 'created_at']
  
  def update(self, instance, validated_data):
    avatar = validated_data.get('avatar', instance.avatar)
    bio = validated_data.get('bio', instance.bio)
    instance.avatar = avatar
    instance.bio = bio
    instance.save()
    return instance

class ChatHistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = ChatHistory
    fields = ['id', 'message', 'is_bot', 'timestamp']