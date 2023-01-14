import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm import tqdm

url = 'https://understat.com/league/EPL'

#Use requests to get the webpage and BeautifulSoup to parse the page
res = requests.get(url)
soup = BeautifulSoup(res.content, features= 'lxml')
scripts = soup.find_all('script')

#print (len(scripts))

## Scrape Fixtures data
strings = scripts[1].string
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')

#convert string to json format
data = json.loads(json_data)
with open("fixtures_data.json", "w") as outfile:
    json.dump(data, outfile)



### Scrape teams data
strings = scripts[2].string
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')

#convert string to json format
data = json.loads(json_data)
with open("teams_data.json", "w") as outfile:
    json.dump(data, outfile)

with open('teams_data.json','r') as f:
    teams_data_json = json.load(f)


##### Scrape Player data
res = requests.get(url)
soup = BeautifulSoup(res.content, features= 'lxml')
scripts = soup.find_all('script')

strings = scripts[3].string
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')

#convert string to json format
data = json.loads(json_data)

with open("players_data.json", "w") as outfile:
    json.dump(data, outfile)

