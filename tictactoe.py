#!/usr/bin/env python

import sys
import signal
import random


def handler(sig, frame):
    """Handles ctrl-c keyboard interrupt"""
    print('\b\b\nOkay, quitter....')
    exit(1)


signal.signal(signal.SIGINT, handler)


RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36


def color_text(text, code=39):
    if text == 'X':
        code = RED
    if text == 'O':
        code = GREEN
    return f"\033[{code}m{text}\033[0m"


def print_board(board):
    '''Prints a TIC-TAC-TOE board, but of any desired size'''
    max_digit_size = len(str(len(board)**2))
    for i in range(len(board)):
        if i > 0:
            print('')
            board_length = len(board) * (3 + max_digit_size)
            print('-' * board_length)
        for j in range(len(board[i])):
            piece = board[i][j] if board[i][j] else f'{
                i*len(board) + j:0{max_digit_size}}'
            if j != 0 and j != len(board[i])-1:
                print(f" {color_text(piece)} ", end='|')
            elif j == 0:
                print(f" {color_text(piece)} ", end='|')
            else:
                print(f" {color_text(piece)} ", end='')
    print('\n\n')


def update(board, player):
    '''Takes a board and a player, asks for player input. Validates input and calculates the row,column (i,j) positions for the piece the player wants to place.'''
    length = len(board)
    while True:
        move = ''
        if player['computer']:
            move = random.randint(0, length)
        else:
            move = input(
                f'\n{player['name']}: Enter a move [0-{length**2 - 1}]: ')
            if move and move.isdigit():
                move = int(move)
                if move > length**2 - 1:
                    print('Out of range!')
                    continue
            else:
                continue
        i, j = move // len(board), move % len(board)
        # print(i, j)
        if board[i][j]:
            if not player['computer']:
                print(f'Problem: Position: {
                      move} is already taken! {board[i][j]}')
            continue
        board[i][j] = player['piece']
        return board
        print('Only valid digits and locations!!')


def check_row(board_row, p1, p2):
    piece = ' '
    for i, p in enumerate(board_row):
        if not p:
            return False
        if i == 0:
            piece = p
        if p != piece:
            return False
    if piece == p1['piece']:
        return p1
    return p2


def win(board, p1, p2) -> bool:
    '''
    Checks the win condition
    First: We gather the rows to check, then the columns, then the two diagonals
    Second: We go through all possible conditions and check if there is a "win" conidtion where all elements are the same
    If there isn't but all positions are taken in that condition then we increment the tie condition.
    If the tie condition is met for all conditions, we end in a tie.
    '''
    length = len(board)
    conditions = [r for r in board]
    cols = [[board[i][j] for i in range(length)] for j in range(length)]
    ldiags = [[board[i][i] for i in range(length)]]
    rdiags = [[board[i][length - 1 - i] for i in range(length)]]
    conditions.extend(cols + rdiags + ldiags)
    # print(conditions)
    tie_condition = 0
    for cond in conditions:
        if all(cond):
            tie_condition += 1
        winner = check_row(cond, p1, p2)
        if winner:
            global WINNER
            WINNER = winner
            print(color_text('-'*20, CYAN))
            print(color_text(f'Winner! {winner['name']}', CYAN))
            print(color_text('-'*20, CYAN))
            return True
    if tie_condition == len(conditions):
        print(color_text('-'*20, YELLOW))
        print(color_text("It's a tie!"), YELLOW)
        print(color_text('-'*20, YELLOW))
        return True
    return False


def game_loop(board, p1, p2):
    player = p1
    print_board(board)
    while not win(board, p1, p2):
        board = update(board, player)
        print_board(board)
        player = p2 if player == p1 else p1
    print_board(board)


def main():
    length = 3
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            length = int(sys.argv[1])

    board = [[False for i in range(length)] for k in range(length)]
    if length < 3:
        print('Only lengths > 2 can we tic-tac-toe')
        exit(1)
    player1 = {
        'name': input("Player 1's Name: "),
        'piece': 'X',
        'computer': False,
    }
    player2 = {
        'name': 'Computer',
        'piece': 'O',
        'computer': True
    }
    game_loop(board, player1, player2)


main()
