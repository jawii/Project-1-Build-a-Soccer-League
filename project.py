import csv
import random
#'Soccer Experience': 
#'Height' (inches)': '44', 
#'Guardian Name(s)': 'Aaron and Jill Finkelstein' 
#'Name': 'Ben Finkelstein'

league = []
sharks = []
dragons = []
raptors = []

# Reads the csv-file
with open('soccer_players.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        league.append(row)

def print_players(lst, team_name):
    print ("There are {} players in {}".format(len(lst), team_name))
    print ("")
    for player in lst:
        print ("Name: ", player['Name'])
        print ("XP: ", player['Soccer Experience'])
        print ("Height (inches): ", player['Height (inches)'])
        print ("Guardian Name(s): ", player['Guardian Name(s)'])
        print ("")
        
def split_list(lst, parts):
    return [lst[0::parts] for i in range(parts)]
     
def make_teams(league, num_teams):   
    #take experienced players
    xpPlayers = []
    for player in league:
        if player['Soccer Experience'] == 'YES':
            xpPlayers.append(player) 

    #move experienced players from league to end of list
    for player in xpPlayers:
        league.remove(player)
        league.append(player)
    #print_players(league)
    
    #make teams
    teams = split_list(league, num_teams)
    
    return (team for team in teams)
    
    
raptors, dragons, sharks = make_teams(league, 3)

#print_players(raptors, "raptors")
#print_players(dragons, "dragons")
#print_players(sharks, "sharks")

def write_letter(player):
    letter = "Dear "
    letter += player

    return letter
print_players(league, "league")
print (league)

