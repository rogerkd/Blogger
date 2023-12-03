import json
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from chat.models import ChatRoom, Messages
from chat.forms import ChatRoomForm, MessagesForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView
from  django.utils.timezone import make_aware


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


class ViewRoom(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat/home.html'
    context_object_name = 'view_room'


def Save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        if len(data) == 2:
            content = data.get("content")
            room = data.get("room_name")
            user = request.user

            chatroom = ChatRoom.objects.get(room_name=room)
            message = Messages(room=chatroom, user=user, content=content)
            message.save()
            return JsonResponse({'status': 'success'})
        
        elif len(data) == 1:
            room = data.get("room_name")
            if ChatRoom.objects.filter(room_name=room).exists():
                return JsonResponse({'status' : 'already_taken'})
            else:
                chatroom = ChatRoom(room_name=room)
                chatroom.save()
                return JsonResponse({'status' : 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

def Remove(request, room):
        try:
            chatroom = ChatRoom.objects.get(room_name=room)
            chatroom.delete()
            return redirect('view_room')
        except ChatRoom.DoesNotExist:
            return HttpResponse("Room not found", status=404)
        

    
class Room(LoginRequiredMixin, ListView):
    model = Messages
    template_name = 'chat/room.html'
    context_object_name = 'view_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # list of rooms
        context['room_name'] = self.kwargs['room_name']
        
        # Room specific messages
        room_id = ChatRoom.objects.get(room_name=context['room_name']).id
        context['view_message'] = context['view_message'].filter(room = room_id)

        # logged-in-user specific messages
        context['user_message'] = context['view_message'].filter(user = self.request.user.id)

        # d
        context['date'] = context['view_message'].values_list('timestamp__date', flat=True)
        context['date'] = list(set(context['date']))
        context['date'].sort()
        # context['date'] = [make_aware(date) for date in context['date']]

        return context


    
    


    
