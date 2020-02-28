# getSongData.py
# gets song data based on country
# Charlie Jindra and Seth Haugland 2/28/2020

import os
import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError

#get username and scope
username =  "charlessjindra"
# sys.argv[1]
scope = 'user-modify-playback-state user-top-read playlist-modify-public user-read-currently-playing playlist-read-collaborative'

#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

#print('well we got past the stupid junk')
#set up spotify object
spotifyObj = spotipy.Spotify(auth=token)

countryFile = open("countryCodes.txt", "r")

# do this for every country
for line in countryFile:
    print("Country: {}".format(line))
    line = line.strip("\n")
    results = spotifyObj.new_releases(country=line, limit=20, offset=0)


    #add all the album ids to one place (albumList) so we can make api calls for the track ids
    albumList = []
    #print(json.dumps(results, indent=4))
    i = 0
    #print(json.dumps(results["albums"]["items"], indent=4))
    print("getting latest albums...")
    for item in enumerate(results["albums"]["items"]):
        #print(item[1]["id"])
        albumList.append(item[1]["id"])
        i = i + 1
    #print(resultsList)

    # now create empty song list to fill with track ids
    songList = []

    print("getting songs from albums...")
    #loop thru albumList
    for album in albumList:
        #get tracks
        results = spotifyObj.album_tracks(album, limit=50)
    #print(results["items"])
        #loop thru each album's tracks to scrape track ids
        for item in enumerate(results["items"]):
            #print(item[1]["id"])
            songList.append(item[1]["id"])
            i = i + 1
            # print(songList)

    #initially set it to 50 less so then they iterate to the correct places the first time
    analyzeUpper = 0
    analyzeLower = -50
    weDone = False

    #amount of tracks we're averaging
    amount = 0

    print("size of tracklist: " + str(len(songList)))
    #the totals that we'll divide by amount later to get averages for the country
    danceTotal, energyTotal, loudnessTotal, speechinessTotal, acousticnessTotal, instrumentTotal, livenessTotal, valenceTotal, tempoTotal = 0, 0, 0, 0, 0, 0, 0, 0, 0

    while(not weDone):
        analyzeLower = analyzeLower + 50
        analyzeUpper = analyzeUpper + 50
        print(str(analyzeUpper) + " > " + str(len(songList)))
        # once we get to where its out of bounds, correct it so its not, and then run it one last time
        if (analyzeUpper > len(songList)):
            weDone = True
            analyzeUpper = len(songList)
        if(analyzeLower > len(songList)-1):
            analyzeLower = len(songList)-1
        #get the JSON for these songs yay
        features = spotifyObj.audio_features(songList[analyzeLower:analyzeUpper])
    
        #now go through the features json one by one to scrape the data
        for item in enumerate(features):
            #print(item[i]['tempo'])
            #print(json.dumps(item, indent=4))
            isAnObject = False
            #print("getting song {} of {}...".format(amount+1, len(songList)))

            #add all these to the totals for the country
            #we'll try to access it, if a value doesn't exist we won't count the song towards the total
            try:
                check = item[1]['danceability']
                check = item[1]['energy']
                check = item[1]['loudness']
                check = item[1]['acousticness']
                check = item[1]['acousticness']
                check = item[1]['instrumentalness']
                check = item[1]['liveness']
                check = item[1]['valence']
                check = item[1]['tempo'] # index 0 bc its a list of features of length 1
                isAnObject = True
            except:
                print("wasnt able to grab a song")

            # only add this songs values if we know that it has all of the ones we want
            if(isAnObject):
                danceTotal = danceTotal + item[1]['danceability']
                energyTotal = energyTotal + item[1]['energy']
                loudnessTotal = loudnessTotal + item[1]['loudness']
                speechinessTotal = speechinessTotal + item[1]['acousticness']
                acousticnessTotal = speechinessTotal + item[1]['acousticness']
                instrumentTotal = instrumentTotal + item[1]['instrumentalness']
                livenessTotal = livenessTotal + item[1]['liveness']
                valenceTotal = valenceTotal + item[1]['valence']
                tempoTotal = tempoTotal + item[1]['tempo'] # index 0 bc its a list of features of length 1
                amount = amount + 1

            #print("tempo total now: " + str(tempoTotal) + "\n\n\n\n\n\n\n\n\n")
            #print("number we at now: " + str(amount))

    #calculate the averages for this country
    #print(amount)
    avgFeatures = {
            "danceability": danceTotal / amount,
            "energy": energyTotal / amount,
            "loudness": loudnessTotal / amount,
            "speechiness": speechinessTotal / amount,
            "acousticness": acousticnessTotal / amount,
            "instrumentalness": instrumentTotal / amount,
            "liveness": livenessTotal / amount,
            "valence": valenceTotal / amount,
            "tempo": tempoTotal / amount
        }

    #finally print the averages with the country code as its name!
    countryWrite = open("data/{}.txt".format(line), "w+")

    for item in avgFeatures:
        countryWrite.write(str(avgFeatures[item]) + "\n")