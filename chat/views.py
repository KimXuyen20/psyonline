from django.shortcuts import render

# Create your views here.
def chat_view(request):
    return render(request, 'chat/chat.html')


def home_view(request):
    return render(request, 'chat/home_chat.html')