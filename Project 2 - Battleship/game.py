import constants
import board
import logging
logging.basicConfig(filename='game_debug.log', level=logging.DEBUG)

logging.debug('DEBUGGIN STARTED')


class Game(object):
    def __init__(self):
        self.player1_board = board.Board()
        self.player1_guess_board = board.Board()
        self.player2_board = board.Board()
        self.player2_guess_board = board.Board()

    def ask_names(self):
        '''
        Asks player names and stores them to objcet.
        '''
        self.player1_name = input("Type Player 1 name: ")
        self.player2_name = input("Type Player 2 name: ")

    def clear_screen(self):
        print("\033c", end="")

    def print_turn(self, player_name):
        self.clear_screen()

        turn_string = "----------------------------- \n"
        turn_string += player_name + "'s" + " turn. \n"
        turn_string += "----------------------------"
        print(turn_string)

        enter_to_continue()

        self.clear_screen()

    def are_ships_left(self, board):
        '''
        Returns True if ships left
        Returns False if no ships left
        '''
        ship_marks = [
            board.vertical_ship_mark,
            board.horizontal_ship_mark
            ]

        are_ship = False

        for place in board.board:
            # print("Place is: " + str(place))
            for mark in place:
                # print("Mark is: " + str(mark))
                if mark in ship_marks:
                    are_ship = True
        return are_ship

    def check_win(self, player1board, player1name, player2board, player2name):
        '''
        If game is over return tuple (False, Winner_name)
        If game is not over returns (True, "")
        '''
        if not self.are_ships_left(player1board):
            return (False, player2name)
        elif not self.are_ships_left(player2board):
            return (False, player1name)
        else:
            return (True, "")

    def start_game(self):
        self.clear_screen()
        print("**************************")
        print("")
        print("Welcome to Battleship game")
        print("")
        print("**************************")
        print("")
        print("Board Size is " + str(constants.BOARD_SIZE))
        print(
            "Marks are: \nVertical ship mark: {} \nHorizontal ship mark: {}\n"
            "Empty mark: {} \nMiss mark: {} \nHit mark: {} \n"
            "Sunk mark: {}".format(
                    constants.VERTICAL_SHIP,
                    constants.HORIZONTAL_SHIP,
                    constants.EMPTY,
                    constants.MISS,
                    constants.HIT,
                    constants.SUNK
                    )
                )
        print("")

        self.ask_names()

        self.clear_screen()
        self.print_turn(self.player1_name)
        self.player1_board.set_ships(self.player1_name)
        self.print_turn(self.player2_name)
        self.player2_board.set_ships(self.player2_name)

        winner_info = self.check_win(
                            self.player1_board,
                            self.player1_name,
                            self.player2_board,
                            self.player2_name
                            )

        while winner_info[0]:

            self.print_turn(self.player1_name)
            attack(
                self.player1_board,
                self.player2_board,
                self.player1_guess_board,
                self.player1_name
                )

            self.clear_screen()

            winner_info = self.check_win(
                                    self.player1_board,
                                    self.player1_name,
                                    self.player2_board,
                                    self.player2_name
                                    )

            if not winner_info[0]:
                break

            self.print_turn(self.player2_name)
            attack(
                self.player2_board,
                self.player1_board,
                self.player2_guess_board,
                self.player2_name
                )

            self.clear_screen()

            winner_info = self.check_win(
                                self.player1_board,
                                self.player1_name,
                                self.player2_board,
                                self.player2_name
                                )

        print("")
        print("***************************")
        print("Game over!")
        print("Winner is: " + winner_info[1])
        print("***************************")
        print("")

        print("Player: {} board was:".format(self.player1_name))
        print(self.player1_board)
        print("Player: {} board was:".format(self.player2_name))
        print(self.player2_board)


def attack(own_board, board_to_attack, guess_board, player1_name):

        turn = True

        while turn:
            print("")
            print("Welcome " + player1_name)
            print("")
            print("Your Guess Board is below")
            print(guess_board)
            print("")

            print("")
            print("Your own Board is below")
            print("")
            print(own_board)
            print("Give attack (col, row) coordinates: ")
            print("")
            attack_coordinate = input("--->")

            check_attack = attack_response(
                                    attack_coordinate,
                                    board_to_attack,
                                    guess_board
                                    )

            if check_attack[0]:
                # check what check_attack returns
                response = check_attack[1]

                # if returns hit or miss, update board places
                if response == "hit":
                    guess_board.set_coord_mark(check_attack[2], "hit")
                    board_to_attack.set_coord_mark(check_attack[2], "hit")
                    print("--------------------")
                    print("You hitted the ship!")
                    print("--------------------")
                    turn = False

                elif response == "miss":
                    guess_board.set_coord_mark(check_attack[2], "miss")
                    board_to_attack.set_coord_mark(check_attack[2], "miss")
                    print("--------------------")
                    print("You missed")
                    print("--------------------")
                    turn = False

                elif response == "sunk":
                    print("--------------------")
                    print("You sunked a ship!!")
                    print("--------------------")
                    turn = False

                elif response == "hitted":
                    print("--------------------")
                    print("You have alredy attacked on that position!")
                    print("--------------------")
                    enter_to_continue()
                    continue
            else:
                print("\033c", end="")
                print(check_attack[1])
            enter_to_continue()
            logging.debug(str(board_to_attack.ships_coordinates))


def attack_response(coordinate, enemy_board, guess_board):
    '''
    Returns (True, "hit"/"miss"/"sunk"/"hitted", (row, col)) or
            (False, "errorstring")
    '''

    coordinate_info = enemy_board.is_coord_in_board(coordinate)

    # check if coordinate is valid
    if not coordinate_info[0]:
        return (False, coordinate_info[1])

    coordinate_mark = enemy_board.get_coord_info(coordinate_info[1])

    # check if there is empty place in board at coordinate
    if coordinate_mark == enemy_board.empty_mark:
        return (True, "miss", coordinate_info[1])

    hitted_marks = [
                enemy_board.hit_mark,
                enemy_board.sunk_mark,
                enemy_board.miss_mark
                ]
    if coordinate_mark in hitted_marks:
        return (True, "hitted", coordinate_info[1])

    hit_mark_1 = coordinate_mark == enemy_board.vertical_ship_mark
    hit_mark_2 = coordinate_mark == enemy_board.horizontal_ship_mark
    hit = hit_mark_1 or hit_mark_2

    if hit:
        logging.debug("Noticed hit!")
        logging.debug("(row, col) is {}".format(coordinate_info[1]))
        # print("Coordinate mark is: " + str(coordinate_info[1]))
        # print("Ship coordinates are: " + str(enemy_board.ships_coordinates))
        # locate ship and remove the length
        for ship in enemy_board.ships_coordinates:
            if coordinate_info[1] in ship:
                # length is second on the list
                ship[1] -= 1
                logging.debug("Removed ship length")
        # check for sunkness
        for ship in enemy_board.ships_coordinates:
            if ship[1] == 0:
                # set all ship marks to sunk and then return sunkness
                coords = ship[2:]
                for coord in coords:
                    enemy_board.set_coord_mark(coord, "sunk")
                    guess_board.set_coord_mark(coord, "sunk")
                # remove ship from coordinate list
                enemy_board.ships_coordinates.remove(ship)

                return (True, "sunk", coordinate_info[1])

        return(True, "hit", coordinate_info[1])


def enter_to_continue():
    while True:
            continue_ = input("Press Enter to Continue \n")
            if continue_ == "":
                break

game = Game()
game.start_game()
