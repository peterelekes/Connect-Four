from django.urls import path
from . import views

urlpatterns = [
    path('start_session/', views.start_session, name='start_session'),
    path('menu/', views.menu, name='menu'),
    path('play/<int:game_id>/', views.play_game, name='play_game'),
    path('end_session/', views.end_session, name='end_session'),
]
