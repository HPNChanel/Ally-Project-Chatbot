from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
  def create_user(self, username, email, full_name, password=None):
    if not email:
      raise ValueError("Email is required")
    if not username:
      raise ValueError("Username is required")

    email = self.normalize_email(email)
    user = self.model(username=username, email=email, full_name=full_name)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, username, email, full_name, password=None):
    user = self.create_user(username, email, full_name, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
  
class CustomUser(AbstractBaseUser, PermissionsMixin):
  full_name = models.CharField(max_length=255)
  username = models.CharField(max_length=150, unique=True)
  email = models.EmailField(unique=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = CustomUserManager()
  
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email', 'full_name']  #* Required to add to field, username as key of table
  
  def __str__(self):
    return self.username

class UserProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
  bio = models.TextField(null=True, blank=True)
  create_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Profile of {self.user.username}"

class ChatHistory(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  message = models.TextField()
  is_bot = models.BooleanField(default=False)  #* Determine message from user or bot
  timestamp = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.username} - {'Bot' if self.is_bot else 'User'}: {self.message[:30]}"
  
class UserSettings(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  reminders_enabled = models.BooleanField(default=True)
  reminder_time = models.TimeField(null=True, blank=True)  #* Reminder time
  reminder_message = models.TextField(default="Don't forget to take a break!")  #* Content of reminder
  
  def __str__(self):
    return f"Settings for {self.user.username}"
