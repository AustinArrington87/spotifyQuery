import requests
import csv
import pandas as pd
import os
import re
import statistics
import operator
import matplotlib.pylab as plt
# create app & get creds: https://developer.spotify.com/dashboard/

CLIENT_ID = os.environ['client_id']
CLIENT_SECRET = os.environ['client_secret']
AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

#  read about audio features here 
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/ 
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# export playlist# https://rawgit.com/watsonbox/exportify/master/exportify.html
# ingest CSV with Top 2018 playlist info 
data = pd.read_csv('charts_2020.csv')
#print(data.head(3))

# collect URIs from CSV
URIs = list(data['uri'].values)
trackIDs = []

#extract the track_id from uri string
for uri in URIs:
    indices = [x.start() for x in re.finditer(":", uri)]
    t_id = uri[indices[2-1]+1:]
    trackIDs.append(t_id)
    
danceList = []
danceStat = []
bpmStat = []
# for each track_id 
for track_id in trackIDs:
    danceDic = {}
    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
    r = r.json()
    # audio features
    dance = r['danceability']
    danceStat.append(dance)
    # tempo
    tempo = r['tempo']
    bpmStat.append(tempo)
    # key
    key = r['key']
    if key == 0:
        key = "C"
    elif key == 1:
        key = "C#/Db"
    elif key == 2:
        key = "D"
    elif key == 3:
        key = "D#/Eb"
    elif key == 4:
        key = "E"
    elif key == 5:
        key = "F"
    elif key == 6:
        key = "F#/Gb"
    elif key == 7:
        key = "G"
    elif key == 8:
        key = "G#/Ab"
    elif key == 9:
        key = "A"
    elif key == 10:
        key = "A#/Bb"
    elif key == 11:
        key = "B"
    else:
        key = "None"
    # song name
    s = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers)
    try:
        s = s.json()['name']
    except:
        s = "Unknown"
    print(s+"____"+str(dance))
    print("tempo: "+str(tempo)+" | " + "key: " +str(key))
    danceDic["song"] = s
    danceDic["danceability"] = dance
    danceDic['tempo'] = tempo
    danceDic['key'] = key
    danceList.append(danceDic)

danceMin = min(danceStat)
danceMax = max(danceStat)
danceMean = round(statistics.mean(danceStat),2)
bpmMin = min(bpmStat)
bpmMax = max(bpmStat)
bpmMean = round(statistics.mean(bpmStat),2)
print("-----------------------------------")
print("Min Danceability:", danceMin, "| Min BPM:", bpmMin)
print("Max Danceability:", danceMax, "| Max BPM:", bpmMax)
print("Mean Danceability:", danceMean, "| Mean BPM:", bpmMean)
# now sort dic and find top 5 songs in terms of danceability
newlist = sorted(danceList, key=lambda k: k['danceability']) 
topTenList = newlist[-5:]
print("-----------------------------------")
print("Top 5 2020 Tracks for Danceability & Tempo")
topTenSong = []
topTenScore = []
topTenTempo = []
for i in topTenList:
    print(i['song'], '| DanceScore:', i['danceability'], '| BPM:', i['tempo'])
    topTenSong.append(i['song'])
    topTenScore.append(i['danceability'])
    topTenTempo.append(i['tempo'])

plt.rcParams["figure.figsize"] = (8, 4)
plt.rcParams["xtick.labelsize"] = 7
plt.bar(topTenSong, topTenScore)
# reshape - 8 wide by 4 high - so text doesn't overlap
plt.xlabel('Song')
plt.ylabel('Danceability')
plt.title('2020 Top 5 Songs for Dancing')
plt.show()
plt.bar(topTenSong, topTenTempo)
plt.xlabel('Song')
plt.ylabel('Tempo')
plt.title('2020 Top 5 Songs BPM')
plt.show()






