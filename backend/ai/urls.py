
from django.urls import path
from .views import GPT4ResponseAPI

urlpatterns = [
  path('gpt4/', GPT4ResponseAPI.as_view(), name='gpt4_response'),
]
