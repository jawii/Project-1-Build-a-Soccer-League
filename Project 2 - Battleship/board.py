import battleship

class Board(object):
	"""Board class for battleship - game"""
	
	def __init__(self):

		self.rows = ['0' * battleship.BOARD_SIZE] * battleship.BOARD_SIZE
		
		