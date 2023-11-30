from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
import openai
import os
from .models import Conversation
from rest_framework.throttling import ScopedRateThrottle

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatbotView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'chatbot'

    def get(self, request):
        user = request.user
        conversations = request.session.get('conversations', [])
        return Response({'conversations': conversations}, status=status.HTTP_200_OK)

    def post(self, request):
        prompt = request.data.get('prompt')
        if prompt:
            user = request.user

            # 이전 대화 기록 가져오기
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = Conversation(prompt=prompt, response=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            request.session.modified = True

            return Response({'prompt': prompt, 'response': response}, status=status.HTTP_200_OK)
        return Response({'error': 'Prompt field is required.'}, status=status.HTTP_400_BAD_REQUEST)
    


class ClearChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        try:
            return Response({'message': '대화가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': '삭제에 실패하였습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
