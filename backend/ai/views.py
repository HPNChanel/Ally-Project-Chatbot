from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ai.services.ai_service import get_gpt4_response

class GPT4ResponseAPI(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    user_message = request.data.get('message', '')
    if not user_message:
      return Response({"error": "Message is required"}, status=400)
    
    user_id = request.user.id
    bot_response = get_gpt4_response(user_message, user_id)
    
    return Response({"response": bot_response}, status=200)