import constants
from board import Board
from ships import ShipInfo


class Game(object):
	def __init__(self):
		self.player1_board = Board()
		self.player2_board = Board()

	def ask_names(self):
		self.player1_name = input("Type Player 1 name: ")
		self.player2_name = input("Type Player 2 name: ")

	def start_game(self):
		print("**************************")
		print("Welcome to Battleship game")
		self.ask_names()

		player1_board.set_ships()
		player2_board.set_ships()

Game().start_game()




