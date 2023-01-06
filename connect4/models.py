from typing import Union

from django.db import models
import random
import json

class MakeMoveMessage:
    def __init__(self, column: int):
        self.column = column

    def __str__(self):
        return f'Made move on column {self.column}'

class WinnerMessage:
    def __init__(self, winner: str):
        self.winner = winner

    def __str__(self):
        return f'Winner is  {self.winner}'


class ConnectFourGame(models.Model):
    game_time = 0
    game_over = models.BooleanField(default=False)
    winner = models.CharField(max_length=1, blank=True)
    vs_computer = models.BooleanField(default=False)
    current_player = models.CharField(max_length=1, default='R')
    board = models.JSONField(default=[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ']])

    def make_move(self, message: MakeMoveMessage):
        # convert self.board to 6*7 matrix of chars
        column = message.column
        board = self.board
        for row in reversed(range(6)):
            if board[row][column] == ' ':
                # Update the board
                board[row][column] = self.current_player
                break
        self.board = board
        self.current_player = 'Y' if self.current_player == 'R' else 'R'

        print(">>MESSAGE: Player " + self.current_player + ": " + str(message) + " and row " + str(row))

        return True

    def check_for_winner(self) -> Union[WinnerMessage, bool]:
        board = self.board
        for row in range(6):
            for column in range(4):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row][column + 1] == board[row][column + 2] == board[row][column + 3]:
                    self.winner = board[row][column]
                    self.game_over = True
                    winner_message = WinnerMessage(winner=self.winner)
                    print(">>MESSAGE: " + str(winner_message))
                    return winner_message
        for row in range(3):
            for column in range(7):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row + 1][column] == board[row + 2][column] == board[row + 3][column]:
                    self.winner = board[row][column]
                    self.game_over = True
                    winner_message = WinnerMessage(winner=self.winner)
                    print(">>MESSAGE: " + str(winner_message))
                    return winner_message
        for row in range(3):
            for column in range(4):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] == board[row + 3][
                    column + 3]:
                    self.winner = board[row][column]
                    self.game_over = True
                    winner_message = WinnerMessage(winner=self.winner)
                    print(">>MESSAGE: " + str(winner_message))
                    return winner_message
        for row in range(3, 6):
            for column in range(4):
                if board[row][column] == ' ':
                    continue
                if board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == board[row - 3][
                    column + 3]:
                    self.winner = board[row][column]
                    self.game_over = True
                    winner_message = WinnerMessage(winner=self.winner)
                    print(">>MESSAGE: " + str(winner_message))
                    return winner_message
        return False

    def make_computer_move(self):
        column = random.randint(0, 6)
        self.make_move(column)
        return column

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'Game {self.id}'



