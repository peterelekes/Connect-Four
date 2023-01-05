from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('play/<int:game_id>/', views.play_game, name='play_game'),
    path('game_over/<int:game_id>/', views.game_over, name='game_over'),
]
