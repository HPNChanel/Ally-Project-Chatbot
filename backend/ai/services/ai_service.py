import openai
from django.core.cache import cache
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_gpt4_response(user_message, user_id):
  cache_key = f"gpt4_response_user_{user_id}_{hash(user_message)}"
  cached_response = cache.get(cache_key)
  
  if cached_response:
    return cached_response
  
  try:
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are a helpful and friendly chatbot."},
        {"role": "user", "content": user_message}
      ],
      max_tokens=150,
      temperature=0.7
    )
    bot_response = response.choices[0].message['content'].strip()

    cache.set(cache_key, bot_response, timeout=300)  #* Save cache in 5 mins
    return bot_response
  
  except Exception as e:
    return "Sorry, I am unable to process your request right now."