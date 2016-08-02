import constants
import ships

class Board(object):
	"""Board class for battleship - game"""
	
	def __init__(self):
		self.vertical_ship_mark = constants.VERTICAL_SHIP
		self.horizontal_ship_mark = constants.HORIZONTAL_SHIP
		self.miss_mark = constants.MISS
		self.hit_mark = constants.HIT
		self.sunk_mark = constants.SUNK
		self.empty_mark = constants.EMPTY
		self.board_size = constants.BOARD_SIZE
		self.board = [[self.empty_mark for x in range(self.board_size)] for y in range(self.board_size)] 
		self.ships = ships.ship_info.ships

	def print_board_heading(self):
		return ("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') + self.board_size)]))

	def __str__(self):

		string = ""
		string += self.print_board_heading() + "\n"
		row_num = 1
		for row in self.board:
			string += (str(row_num).rjust(2) + " " + (" ".join(row))) + "\n"
			row_num += 1
		
		return string
	
	def clear_screen(self):
		print("\033c", end="")

	def ask_coordinates(self, ship):

			alpabets = [chr(c) for c in range(ord('a'), ord('a') + self.board_size)]

			while True:
				coordinate = input("Place the location (col, row) of the " + ship[0] + " (" + str(ship[1]) + " spaces): " )
				coordinate = coordinate.replace(" ","")
				coordinate = (coordinate[0], coordinate[1:])
				#print(coordinate)
				try:
					row = int(coordinate[1])
					if row not in list(range(self.board_size + 1)):
						self.clear_screen()
						print("")
						print("Incorrect coordinate. Row number too high!")
						print("")
						print(board)
						continue
				except ValueError:
					self.clear_screen()
					print("")
					print("Can't find the row. Type col first and then row. For Example 'a1'")
					print("")
					print(board)
					continue

				if coordinate[0].lower() not in alpabets:
					self.clear_screen()
					print("")
					print("Incorrect coordinate. Can't find the column. Type column first and then row.")
					print("")
					print(board)
					continue
				else:
					break
				
			row = int(coordinate[1]) - 1
			col = alpabets.index(coordinate[0])

			return (row, col)

	def ask_orient(self):
			horizontal = True
			is_horizontal= ""
			while True:
				is_horizontal = input("Is it horizontal? (Y)/N: ")
				if is_horizontal.lower() == 'y':
					horizontal = True
					break
				elif is_horizontal.lower() == 'n':
					horizontal = False 
					break

			return horizontal

	def place_ship(self, row_col, ship_length, is_horizontal):
		
		row = row_col[0]
		col = row_col[1]

		if is_horizontal:
			mark = self.horizontal_ship_mark
			for place in range(ship_length):
				self.board[row][col + place] = mark
		else:
			mark = self.vertical_ship_mark
			for place in range(ship_length):
				self.board[row + place][col] = mark


	def can_ship_set(self, row_col, ship_length,is_horizontal):
		
		error_string = "\n You can't place ship there.\n"
		forbidden_places = [self.horizontal_ship_mark, self.vertical_ship_mark]
		if row_col == None:
			return (True, "")

		else:
			row = row_col[0]
			col = row_col[1]
			place = 0
			if is_horizontal:
				dummy_1 = col
				dummy_2 = row
				dummy_3 = col + place
			else:
				dummy_1 = row
				dummy_2 = row + place
				dummy_3 = col

			is_space = dummy_1 <= self.board_size - ship_length
			are_there_ships = False

			try:
				for place in range(ship_length):
					if self.board[dummy_2][dummy_3] in forbidden_places:
						are_there_ships = True
						error_string = " \n You can't place ship there. There is already a ship. \n"
			except IndexError:
				are_there_ships = False

			if is_space and not are_there_ships:
				return (False, "")
			else:
				return (True, error_string)

	def set_ships(self):
		
			for ship in self.ships:

				row_col = None
				is_horizontal = None
				ship_length = None

				can_set = self.can_ship_set(row_col, ship_length, is_horizontal)

				while can_set[0]:
					print(board)
					row_col = self.ask_coordinates(ship)
					is_horizontal = self.ask_orient()
					ship_length = ship[1]
					can_set = self.can_ship_set(row_col, ship_length, is_horizontal)
					if can_set[0]:
						self.clear_screen()
						print(can_set[1])

				self.place_ship(row_col, ship_length, is_horizontal)
				self.clear_screen()
			print(board)



#board = Board()
#print(board.board)
#board.set_ships()


		