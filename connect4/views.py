import time

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import ConnectFourGame, MakeMoveMessage

current_time = 0
session_time = 0

def start_session(request):
    global session_time
    if request.method == 'GET':
        session_time = time.time()
        print(">>MESSAGE: Session started.")
        response = redirect('menu')
        response.set_cookie('session_time', session_time)
        return response

def menu(request):
    global current_time
    if request.method == 'POST':
        if 'pvp' in request.POST:
            game = ConnectFourGame.objects.create(vs_computer=False)
            print(">>MESSAGE: Player vs Player game started.")
            current_time = time.time()
            game.game_time = current_time
            return redirect('play_game', game_id=game.id)
        elif 'vs_computer' in request.POST:
            game = ConnectFourGame.objects.create(vs_computer=True)
            print(">>MESSAGE: Player vs Computer game started.")
            current_time = time.time()
            game.game_time = current_time
            return redirect('play_game', game_id=game.id)
    return render(request, 'menu.html')


def play_game(request, game_id):
    game = get_object_or_404(ConnectFourGame, pk=game_id)
    player = game.current_player
    if game.game_over:
        global current_time
        game.game_time = '{:.2f}'.format(float(time.time() - current_time))
        print(">>MESSAGE: Game ended. Lasted: " + str(game.game_time) + " seconds")
    #check if pvp or vs computer
    if game.vs_computer:
        if game.current_player == 'Y':
            game.make_computer_move()
            game.check_for_winner()
            game.save()
            return redirect('play_game', game_id=game.id)
        if request.method == 'POST':
            column = int(request.POST['column'])
            message = MakeMoveMessage(column=column)
            game.make_move(message)
            game.check_for_winner()
            game.save()
            return redirect('play_game', game_id=game.id)
    else:
        if request.method == 'POST':
            column = int(request.POST['column'])
            message = MakeMoveMessage(column = column)
            game.make_move(message)
            game.check_for_winner()
            game.save()
            return redirect('play_game', game_id=game.id)
    return render(request, 'play.html', {'game': game, 'player': player})

def end_session(request):
    if request.method == 'POST':
        start_time = request.COOKIES.get('session_time')
        if start_time:
            elapsed_time = time.time() - float(start_time)
            print(">>MESSAGE: Session ended. Elapsed time: " + str('{:.2f}'.format(elapsed_time)) + " seconds.")
            return HttpResponse()  # Return empty response
        else:
            return HttpResponse(">>ERROR: Start time cookie not found.")
