import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm import tqdm

base_url = 'https://understat.com/match/'

def scrape_data(match_id, h_team, a_team, gw):
    match = str(match_id)
    url = base_url+match

    #Use requests to get the webpage and BeautifulSoup to parse the page
    res = requests.get(url)
    soup = BeautifulSoup(res.content, features = "lxml")
    scripts = soup.find_all('script')
    strings = scripts[1].string

    # strip unnecessary symbols and get only JSON data 
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')

    #convert string to json format
    data = json.loads(json_data)

    X = []
    Y = []
    minute = []
    result = []
    player = []
    situation = []
    player_assisted = []
    last_action = []
    team = []
    xG = []
    opp_team = []

    data_home = data['h']
    data_away = data['a']
    #len(data_home), len(data_away)

    for shot_data in data_home:
        X.append(shot_data['X'])
        Y.append(shot_data['Y'])
        minute.append(shot_data['minute'])
        result.append(shot_data['result'])
        player.append(shot_data['player'])
        situation.append(shot_data['situation'])
        player_assisted.append(shot_data['player_assisted'])
        last_action.append(shot_data['lastAction'])
        team.append(shot_data['h_team'])
        opp_team.append(shot_data['a_team'])
        xG.append(shot_data['xG'])


    for shot_data in data_away:
        X.append(shot_data['X'])
        Y.append(shot_data['Y'])
        minute.append(shot_data['minute'])
        result.append(shot_data['result'])
        player.append(shot_data['player'])
        situation.append(shot_data['situation'])
        player_assisted.append(shot_data['player_assisted'])
        last_action.append(shot_data['lastAction'])
        team.append(shot_data['a_team'])
        opp_team.append(shot_data['h_team'])
        xG.append(shot_data['xG'])

    col_names = ["minute", "X", "Y", "Team", "xG","Result","Player","Situation","Player_assisted","lastAction","Opp"]
    data_df = pd.DataFrame([minute, X, Y, team, xG, result, player, situation, player_assisted, last_action, opp_team], index = col_names).T
    data_df.sort_values(by = "minute", inplace = True)

    data_df.to_csv("{}/shot_data_{}.csv".format(gw, match), index = False)

    ## Roster Data
    strings = scripts[2].string
    # strip unnecessary symbols and get only JSON data 
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')

    #convert string to json format
    data = json.loads(json_data)

    roster_data_h = pd.DataFrame(data['h']).T
    roster_data_a = pd.DataFrame(data['a']).T
    roster_data_h.to_csv("{}/roster_data_{}.csv".format(gw, h_team), index = False)
    roster_data_a.to_csv("{}/roster_data_{}.csv".format(gw, a_team), index = False)

#Make sure there is a space after every comma for consistency of this code to run
print ("Input GW matches to scrape:")
gw = "GW" + str(input())
matches = pd.read_csv("{}/matches.txt".format(gw), sep = ", ")
#print (matches.columns)
#print (matches)

for idx, row in tqdm(matches.iterrows()):
    match_id = row['Match ID']
    h_team = row['Home_Team']
    a_team = row['Away_Team']

    #print (match_id, h_team, a_team)
    scrape_data(match_id, h_team, a_team, gw)

    