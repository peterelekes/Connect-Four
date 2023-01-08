from typing import Union

from django.db import models
import random
import json
import math
import copy

COLUMN_COUNT = 7
ROW_COUNT = 6
WINDOW_LENGTH = 4
EMPTY = ' '
PLAYER_PIECE = 'R'
AI_PIECE = 'Y'


def check_for_which_winner(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def drop_piece(board, col, piece):
    for row in reversed(range(6)):
        if board[row][col] == ' ':
            # Update the board
            board[row][col] = piece
            break


def is_valid_location(board, col):
    return board[0][col] == ' '


def get_next_open_row(board, col):
    for r in reversed(range(ROW_COUNT)):
        if board[r][col] == ' ':
            return r


def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE
    if (piece == opponent_piece):
        opponent_piece = AI_PIECE
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 8
    return score


def is_terminal_node(board):
    return check_for_which_winner(board, PLAYER_PIECE) or check_for_which_winner(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def score_position(board, piece):
    # Score horizontal
    score = 0
    center_array = []
    for r in range(ROW_COUNT):
        center_array.append(board[r][COLUMN_COUNT // 2])
    center_count = center_array.count(piece)
    score += center_count * 6
    for r in range(ROW_COUNT):
        row_array = []
        for column in range(COLUMN_COUNT):
            row_array.append(board[r][column])
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score vertical
    for r in range(COLUMN_COUNT):
        col_array = []
        for row in range(ROW_COUNT):
            col_array.append(board[row][r])
        for c in range(ROW_COUNT - 3):
            window = col_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score pozitive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def prettyPrint(board):
    for row in range(ROW_COUNT):
        print("[", end=" ")
        for col in range(COLUMN_COUNT):
            print(board[row][col],end=", ")
        print("]")
    print()

def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_for_which_winner(board, AI_PIECE):
                return (None, 100000)
            elif check_for_which_winner(board, PLAYER_PIECE):
                return (None, -100000)
            else:
                return (None, -100)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def minimax_alphabeta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_for_which_winner(board, AI_PIECE):
                return (None, 100000)
            elif check_for_which_winner(board, PLAYER_PIECE):
                return (None, -100000)
            else:
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, col, AI_PIECE)
            new_score = minimax_alphabeta(b_copy, depth-1, alpha, beta, True)[1]
            if new_score > value:
                value = new_score
                column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                return column, value
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, col, PLAYER_PIECE)
            new_score = minimax_alphabeta(b_copy, depth-1, alpha, beta, False)[1]
            if new_score < value:
                value = new_score
                column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def get_best_move(board, AI_PIECE):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        temp_board = copy.deepcopy(board)
        drop_piece(temp_board, col, AI_PIECE)
        column, score = minimax_alphabeta(temp_board, 3, -math.inf, math.inf, True, AI_PIECE, PLAYER_PIECE)
        if score > best_score:
            best_score = score
            best_col = column
    return best_col




def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = copy.deepcopy(board)
        drop_piece(temp_board, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


class MakeMoveMessage:
    def __init__(self, column: int):
        self.column = column

    def __str__(self):
        return f'Made move on column {self.column + 1}'


class WinnerMessage:
    def __init__(self, winner: str):
        self.winner = winner

    def __str__(self):
        return f'Winner is {self.winner}'


class ConnectFourGame(models.Model):
    game_time = 0
    difficulty = models.IntegerField(default=1)
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
        print(">>MESSAGE: Player " + self.current_player + ": " + str(message) + " and row " + str(row + 1))
        self.current_player = 'Y' if self.current_player == 'R' else 'R'

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
        board_copy = copy.deepcopy(self.board)
        column=minimax(board_copy,self.difficulty,True)[0]
        message = MakeMoveMessage(column=column)
        self.make_move(message)
        return column

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'Game {self.id}'
