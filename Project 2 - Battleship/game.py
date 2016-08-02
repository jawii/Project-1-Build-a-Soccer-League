import constants
import board
from ships import ShipInfo


class Game(object):
    def __init__(self):
        self.player1_board = board.Board()
        self.player1_guess_board = board.Board()
        self.player2_board = board.Board()
        self.player2_guess_board = board.Board()

    def ask_names(self):
        self.player1_name = input("Type Player 1 name: ")
        self.player2_name = input("Type Player 2 name: ")
    
    def clear_screen(self):
        print("\033c", end="")

    def print_turn(self, player_name):
        self.clear_screen()

        turn_string = "----------------------------- \n"
        turn_string += player_name +"'s" + " turn. \n" 
        turn_string += "Press Enter to Continue \n"
        turn_string += "----------------------------"

        while True:
            print(turn_string)
            continue_ = input("")
            if continue_ == "":
                break
        self.clear_screen()

    def check_win(self):
        '''
        If game is over return tuple (Fase, Winner_name)
        If game is not over returns (True, "")
        '''
        return (True, "")


    def start_game(self):
        self.clear_screen()
        print("**************************")
        print("")
        print("Welcome to Battleship game")
        print("")
        print("**************************")
        self.ask_names()

        self.clear_screen()
        self.print_turn(self.player1_name)
        self.player1_board.set_ships(self.player1_name)
        self.print_turn(self.player2_name)
        self.player2_board.set_ships(self.player2_name)

        while self.check_win()[0]:
            
            self.print_turn(self.player1_name)
            attack(self.player1_board, self.player2_board, self.player1_guess_board, self.player1_name)
            self.clear_screen()
            self.print_turn(self.player2_name)
            attack(self.player2_board, self.player1_board, self.player2_guess_board, self.player2_name)
            self.clear_screen()



def attack(own_board, board_to_attack, guess_board, player1_name):

        turn = True

        while turn:

            print("Welcome " + player1_name)
            print("Your Guess Board is below")
            print(guess_board)

            print("Your own Board is below")
            print(own_board)
            print("Give attack (col, row) coordinates: ")
            attack_coordinate = input("--->")
            
            check_attack = attack_response(attack_coordinate, board_to_attack)

            if check_attack[0]:
                # check what check_attack returns
                response = check_attack[1]

                # if returns hit or miss, update board places
                if response == "hit":
                    guess_board.set_coord_mark(check_attack[2], "hit")
                    board_to_attack.set_coord_mark(check_attack[2], "hit")
                    print("You hitted the ship!")

                elif response == "miss":
                    guess_board.set_coord_mark(check_attack[2], "miss")
                    board_to_attack.set_coord_mark(check_attack[2], "miss")
                    print("You missed")

                elif response == "sunk":
                    print("You sunked a ship!!")

                # update player2 board and own guess board
                turn = False
            else:
                print(check_attack[1])



def attack_response(coordinate, enemy_board):
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

    if coordinate_mark == enemy_board.hit_mark or coordinate_mark == enemy_board.sunk_mark:
        return (True, "hitted", coordinate_info[1])

    hit_mark_1 = coordinate_mark == enemy_board.vertical_ship_mark
    hit_mark_2 = coordinate_mark == enemy_board.horizontal_ship_mark
    hit = hit_mark_1 or hit_mark_2

    if hit:
        # print("Coordinate mark is: " + str(coordinate_info[1]))
        # print("Ship coordinates are: " + str(enemy_board.ships_coordinates))
        #locate ship and remove the length
        for ship in enemy_board.ships_coordinates:
            if coordinate_info[1] in ship:
                #length is second on the list
                ship[1] -= 1
        #check for sunkness
        for ship in enemy_board.ships_coordinates:
            if ship[1] == 0:
                #set all ship marks to sunk and then return sunkness
                coords = ship[2:]
                for coord in coords:
                    enemy_board.set_coord_mark(coord, "sunk")
                return (True, "sunk", coordinate_info[1])

        return(True, "hit", coordinate_info[1])


game = Game()
game.start_game()







