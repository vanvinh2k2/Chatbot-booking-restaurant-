from django.urls import path
from .views import index
from .backend import reponse_chatbot, list_chatbot

urlpatterns = [
    path('', index, name="index"),
    path('response/<uid>/', reponse_chatbot, name="respone-ai"),
    path('list-chat/<uid>/', list_chatbot, name="list-chat"),
]