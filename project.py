import csv
import random
from datetime import date
from operator import itemgetter, attrgetter



#'Soccer Experience': 
#'Height' (inches)': '44', 
#'Guardian Name(s)': 'Aaron and Jill Finkelstein' 
#'Name': 'Ben Finkelstein'

league = []
sharks = []
dragons = []
raptors = []
dragons_practise_day = "March 17"
dragons_practise_time = "1pm"
sharks_practise_day = "March 17"
sharks_practise_time = "3pm"
raptors_practise_day = "March 18"
raptors_practise_time = "1pm"

# Reads the csv-file
with open('soccer_players.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        league.append(row)

def print_players(lst, team_name):
    print ("There are {} players in {}".format(len(lst), team_name))
    print ("-------------------------")
    print ("")
    for player in lst:
        print ("Name: ", player['Name'])
        print ("XP: ", player['Soccer Experience'])
        print ("Height (inches): ", player['Height (inches)'])
        print ("Guardian Name(s): ", player['Guardian Name(s)'])
        if 'Team name' in player.keys():
            print ("Team name: ", player['Team name'])

        print ("--------------------")
        
def split_list(lst, parts):
    return [lst[i::parts] for i in range(parts)]

def get_average_height(players):
    total_height = 0
    number_of_players = len(players)
    for player in players:
        total_height += int(player['Height (inches)'])
    return total_height / float(number_of_players)

def sort_by_height(players):
    return sorted(players, key = itemgetter('Height (inches)'))

#print_players(align_with_height(league), "League")


def make_teams(league, num_teams):   
    #take experienced players away from league
    xpPlayers = []
    league2 = league[:]
    for player in league:
        if player['Soccer Experience'] == 'YES':
            xpPlayers.append(player)
            league2.remove(player)
    league = league2

    #sort league and xpPlayers by height
    xpPlayers = sort_by_height(xpPlayers)
    league = sort_by_height(league)

    #move experienced players back to league
    for player in xpPlayers:
        league.insert(0, player)
    #print_players(league)
    
    #make teams
    teams = split_list(league, num_teams)

    return tuple(team for team in teams)
    


def write_letter(player):
    letter = "Dear "
    letter += player['Guardian Name(s)'] + ". \n \n"

    player["Team name"] = ""
    if player in raptors:
        player["Team name"] = "Raptors"
        first_practise_day = raptors_practise_time
        first_practise_time = raptors_practise_time
    elif player in dragons:
        player["Team name"] = "Dragons"
        first_practise_day = dragons_practise_day
        first_practise_time = dragons_practise_time
    elif player in sharks:
        player["Team name"] = "Sharks"
        first_practise_day = sharks_practise_day
        first_practise_time = sharks_practise_time

    letter += ("Soccer teams are made. We made teams so that every team" 
            + "has equal amount of experienced players and teams average" 
            + "heights are almost equal \n")

    letter += "Your child " + player['Name'] + " " 
    letter += "plays in team named " + player["Team name"] + "\n"
    letter += "Our first practise will be in " \
            + first_practise_day + " at " + first_practise_time + "."
    letter += "\n" + "See you at the field!"
    return letter

# Update teams to league
for player in league:
    if player in raptors:
        player["Team name"] = "Raptors"
    elif player in dragons:
        player["Team name"] = "Dragons"
    elif player in sharks:
        player["Team name"] = "Sharks"


if __name__ == "__main__":

    dragons, raptors , sharks = make_teams(league, 3)

    #print_players(dragons, "dragons")
    #print_players(raptors, "raptors")
    #print_players(sharks, "sharks")

    league = list(dragons) + list(raptors) + list(sharks)

    # Update teams to league
    for player in league:
        if player in raptors:
            player["Team name"] = "Raptors"
        elif player in dragons:
            player["Team name"] = "Dragons"
        elif player in sharks:
            player["Team name"] = "Sharks"
        else:
            player["Team name"] = "(no team)"
    
    #print_players(league, "League")

    for player in league:
        file_name = player["Name"].replace(" ", "_").lower() + ".txt"
        with open(file_name, "w") as letter:
            letter.write(write_letter(player))

#print_players(dragons, "dragons")
#print_players(raptors, "raptors")
#print_players(sharks, "sharks")

#print (get_average_height(raptors))
#print (get_average_height(dragons))
#print (get_average_height(sharks))