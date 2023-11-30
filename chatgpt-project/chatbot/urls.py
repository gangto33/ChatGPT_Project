from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatbotView.as_view(), name='chat'),
    path('clear/', views.ClearChatView.as_view(), name='clear')
]
