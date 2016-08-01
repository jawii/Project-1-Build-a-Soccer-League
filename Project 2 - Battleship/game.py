import battleship
from board import Board

PLAYER_1 = input("Type player 1 name: ")
PLAYER_2 = input("Type player 2 name: ")

battleship.clear_screen()

board = Board()

battleship.print_board(board.rows)

print(board.rows)