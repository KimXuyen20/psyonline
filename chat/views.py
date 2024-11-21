from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from chat.models import *

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="group_chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    
    return render(request,'chat/chat.html',{'chat_messages':chat_messages})