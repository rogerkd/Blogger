from django.urls import path
from chat import views
from chat.views import Room, ViewRoom

urlpatterns = [

    path('', ViewRoom.as_view(), name='view_room'),
    path('<str:room_name>/', Room.as_view(), name='room'),
    path('save', views.Save, name='save'),
    path("remove/<str:room>/", views.Remove, name='remove'),
]