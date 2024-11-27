from django.urls import path 
from .views import *

urlpatterns = [
    path('chat/', chat_view,name="chat"),
    path('home_chat/', home_view,name="home_chat"),
]
