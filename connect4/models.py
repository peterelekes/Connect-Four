from django.db import models
import random

class ConnectFourGame(models.Model):
    board = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    game_over = models.BooleanField(default=False)
    winner = models.CharField(max_length=1, blank=True)
    vs_computer = models.BooleanField(default=False)
    current_player = models.CharField(max_length=1, default='R')


    def make_move(self, column):
        board = self.board
        for row in reversed(range(6)):
            if board[row][column] == ' ':
                # Update the board
                board[row][column] = self.current_player
                break
        self.board = board
        self.current_player = 'Y' if self.current_player == 'R' else 'R'
        return True

    def check_for_winner(self):
        board = self.board
        for row in range(6):
            for column in range(4):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row][column + 1] == board[row][column + 2] == board[row][column + 3]:
                    self.winner = board[row][column]
                    self.game_over = True
                    return True
        for row in range(3):
            for column in range(7):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row + 1][column] == board[row + 2][column] == board[row + 3][column]:
                    self.winner = board[row][column]
                    self.game_over = True
                    return True
        for row in range(3):
            for column in range(4):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] == board[row + 3][column + 3]:
                    self.winner = board[row][column]
                    self.game_over = True
                    return True
        for row in range(3, 6):
            for column in range(4):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == board[row - 3][column + 3]:
                    self.winner = board[row][column]
                    self.game_over = True
                    return True
        return False

    def make_computer_move(self):
        column = random.randint(0, 6)
        self.make_move(column)
        return column
    
    def reset_game(self):
        self.board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]
        self.game_over = False
        self.winner = ''
        self.vs_computer = False
        self.current_player = 'R'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __str__(self):
        return f'Game {self.id}'
