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

with open('soccer_players.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        league.append(row)

def print_players(lst):
#prints player lst
    print ("There are {} players.".format(len(lst)))
    print ("")
    for player in lst:
        print ("Name: ", player['Name'])
        print ("XP: ", player['Soccer Experience'])
        print ("Height (inches): ", player['Height (inches)'])
        print ("Guardian Name(s): ", player['Guardian Name(s)'])
        print("")
        
        
def split_list(lst, parts):
    return [lst[0::parts] for i in range(parts)]
     
def make_teams(league, num_teams):
    #shuffle list
    #league = random.shuffle(league)
    #print_players(league)
    
    #take experienced players
    xpPlayers = []
    for player in league:
        if player['Soccer Experience'] == 'YES':
            xpPlayers.append(player) 
    #print_players(xpPlayers)
    
    #move experienced players from league to end of list
    for player in xpPlayers:
        league.remove(player)
        league.append(player)
    #print_players(league)
    
    #make (teams)
    teams = split_list(league, num_teams)
    
    for team in teams:
        print_players(team)
        print ("")
        print ("")
    
    
             
#print_players(league)         
make_teams(league, 2)

