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
            
            check_attack = is_valid_attack(attack_coordinate, board_to_attack)

            if check_attack[0]:
                # return if hit miss or invalid type
                # update player2 board and own guess board
                turn = False
            else:
                print(check_attack[1])



def is_valid_attack(coordinate, enemy_board):
    ''' 
    Returns (True, hit/miss/sunk) or
            (False, "errorstring"))
    '''
    # check if coordinate is valid
    is_coordinate_valid = enemy_board.is_coord_in_board(coordinate)

    print("Enemy Board")
    print (enemy_board)
    print (is_coordinate_valid)

    # check if there is empty place in board at coordinate
    
    return (True, "hit")






game = Game()
game.start_game()


#Test for is_valid_attack






