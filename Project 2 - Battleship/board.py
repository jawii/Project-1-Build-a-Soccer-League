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
        self.board = [
                [self.empty_mark for x in range(self.board_size)]
                for y in range(self.board_size)
                ]
        self.ships = ships.ship_info.ships
        self.ships_coordinates = []

    def print_board_heading(self):
        return ("   " + " ".join([chr(c)
                for c in range(ord('A'), ord('A') + self.board_size)]))

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
        ''' 
        Returns coordinate tuple(row, col)
        '''
        alpabets = [
                chr(c) for c in
                range(ord('a'), ord('a') + self.board_size)
                    ]

        while True:
            coordinate = input(
                    "Place the location (col, row) of the "
                    + ship[0] + " (" + str(ship[1]) + " spaces): "
                    )

            #
            #
            coordinate_info = self.is_coord_in_board(coordinate)

            if coordinate_info[0]:
                return coordinate_info[1]
            else:
                self.clear_screen()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(coordinate_info[1])
                print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("")
                print(self)
                continue

    def ask_orient(self):
            horizontal = True
            is_horizontal = ""
            while True:
                is_horizontal = input("Is it horizontal? (Y)/N: ")
                if is_horizontal.lower() == 'y':
                    horizontal = True
                    break
                elif is_horizontal.lower() == 'n':
                    horizontal = False
                    break

            return horizontal

    def place_ship(self, row_col, ship, is_horizontal):

        row = row_col[0]
        col = row_col[1]
        ship_length = ship[1]
        self.ships_coordinates.append([ship[0]])
        self.ships_coordinates[-1].append(ship[1])

        if is_horizontal:
            mark = self.horizontal_ship_mark
            for place in range(ship_length):
                self.board[row][col + place] = mark
                # update ship coordinates
                self.ships_coordinates[-1].append((row, col + place))
        else:
            mark = self.vertical_ship_mark
            for place in range(ship_length):
                self.board[row + place][col] = mark
                # update ship coordinates
                self.ships_coordinates[-1].append((row, col + place))
            
    def can_ship_set(self, row_col, ship_length, is_horizontal):

        error_string = "\n You can't place ship there.\n"
        forbidden_places = [self.horizontal_ship_mark, self.vertical_ship_mark]
        if row_col is None:
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
                        error_string = (
                            "\n You can't place ship there."
                            + "There is already a ship. \n"
                            )
            except IndexError:
                are_there_ships = False

            if is_space and not are_there_ships:
                return (False, "")
            else:
                return (True, error_string)

    def set_ships(self, player_name):

            for ship in self.ships:

                row_col = None
                is_horizontal = None
                ship_length = None

                can_set = self.can_ship_set(
                        row_col,
                        ship_length,
                        is_horizontal
                        )

                while can_set[0]:
                    print("Put the ships " + player_name)
                    print(self)
                    row_col = self.ask_coordinates(ship)
                    is_horizontal = self.ask_orient()
                    ship_length = ship[1]

                    can_set = self.can_ship_set(
                        row_col,
                        ship_length,
                        is_horizontal
                        )

                    if can_set[0]:
                        self.clear_screen()
                        print(can_set[1])

                self.place_ship(row_col, ship, is_horizontal)
                self.clear_screen()
            #print(self)

    def is_coord_in_board(self, coordinate):
        ''' 
        Checks if player coordinate input is in board
        Returns (False, error_string) if coodinate is not in board
        Returns (True, (row, col)) if coordinate is valid 
        '''
        alpabets = [
            chr(c) for c in
            range(ord('a'), ord('a') + self.board_size)
            ]

        error_string = ""
        coordinate = coordinate.replace(" ", "")
        coordinate = (coordinate[0], coordinate[1:])
        
        try:
            row = int(coordinate[1])
            if row not in list(range(self.board_size + 1)):
                error_string = "Incorrect coordinate. Row number too high!"
                return (False, error_string)
        except ValueError:
            error_string = "Can't find the row. Type col first and then row. For Example 'a1'."
            return (False, error_string)

        if coordinate[0].lower() not in alpabets:
            error_string = "Incorrect coordinate." \
                            "Can't find the column." \
                            "Type column first and then row."
            return (False, error_string)

        row = int(coordinate[1]) - 1
        col = alpabets.index(coordinate[0])
        return (True, (row, col))

    def get_coord_info(self, row_col):
        """
        Returns what mark is in coord:
        """
        row = row_col[0]
        col = row_col[1]

        return self.board[row][col]

    def set_coord_mark(self, row_col, mark):
        '''
        Valid marks: empty, hit, miss, sunk
        Return nothing
        '''
        if mark == "empty":
            _mark = self.empty_mark
        
        elif mark == "hit":
            _mark = self.hit_mark
        
        elif mark == "miss":
            _mark = self.miss_mark
        
        elif mark == "sunk":
            _mark = self.sunk_mark

        row = row_col[0]
        col = row_col[1]

        self.board[row][col] = _mark






# board = Board()
# print(board)
# board.place_ship((1,1), board.ships[1], True)
# board.place_ship((2,1), board.ships[2], True)

# print(board)
# print(board.ships_coordinates)

# print(board.is_coord_in_board("11"))


