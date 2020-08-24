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
# for each track_id 
for track_id in trackIDs:
    danceDic = {}
    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
    r = r.json()
    dance = r['danceability']
    danceStat.append(dance)
    # song name
    s = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers)
    s = s.json()['name']
    print(s+"____"+str(dance))
    danceDic["song"] = s
    danceDic["danceability"] = dance
    danceList.append(danceDic)

danceMin = min(danceStat)
danceMax = max(danceStat)
danceMean = round(statistics.mean(danceStat),2)
print("Min Danceability:", danceMin)
print("Max Danceability:", danceMax)
print("Mean Danceability:", danceMean)
# now sort dic and find top 10 songs in terms of danceability
newlist = sorted(danceList, key=lambda k: k['danceability']) 
topTenList = newlist[-5:]
print("Top 5 2020 Tracks for Danceability")
print("-----------------------------------")
topTenSong = []
topTenScore = []
for i in topTenList:
    print(i['song'] + ':' + str(i['danceability']))
    topTenSong.append(i['song'])
    topTenScore.append(i['danceability'])

plt.rcParams["figure.figsize"] = (8, 4)
plt.rcParams["xtick.labelsize"] = 7
plt.bar(topTenSong, topTenScore)
# reshape - 8 wide by 4 high
plt.xlabel('Song')
plt.ylabel('Danceability')
plt.title('2020 Top 5 Songs for Dancing')
plt.show()












