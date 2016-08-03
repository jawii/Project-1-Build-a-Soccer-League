import constants


class ShipInfo(object):

    def __init__(self):

        self.ships = constants.SHIP_INFO

    def __str__(self):
        ships_string = "Available ships are: \n"
        for ship in self.ships:
            ships_string += " " + ship[0] + ": " + str(ship[1]) + "\n"
        return ships_string

    def get_ship_len(self, ship_name):
        ''' Return ships length '''
        for ship in self.ships:
            if ship_name == ship[0]:
                return ship[1]

ship_info = ShipInfo()
