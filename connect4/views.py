from django.shortcuts import render, redirect, get_object_or_404

from .models import ConnectFourGame

def menu(request):
    if request.method == 'POST':
        if 'pvp' in request.POST:
            game = ConnectFourGame.objects.create(vs_computer=False)
            return redirect('play_game', game_id=game.id)
        elif 'vs_computer' in request.POST:
            game = ConnectFourGame.objects.create(vs_computer=True)
            return redirect('play_game', game_id=game.id)
    return render(request, 'menu.html')


def play_game(request, game_id):
    game = get_object_or_404(ConnectFourGame, pk=game_id)
    player = game.current_player
    if game.game_over:
        return redirect('game_over', game_id=game.id)
    #check if pvp or vs computer
    if game.vs_computer:
        if game.current_player == 'Y':
            game.make_computer_move()
            game.check_for_winner()
            game.save()
            return redirect('play_game', game_id=game.id)
        if request.method == 'POST':
            column = int(request.POST['column'])
            game.make_move(column)
            game.check_for_winner()
            game.save()
            return redirect('play_game', game_id=game.id)
    else:
        if request.method == 'POST':
            column = int(request.POST['column'])
            game.make_move(column)
            game.check_for_winner()
            game.save()
            return redirect('play_game', game_id=game.id)
    return render(request, 'play.html', {'game': game, 'player': player})

def game_over(request, game_id):
    game = get_object_or_404(ConnectFourGame, pk=game_id)
    return render(request, 'game_over.html', {'game': game})