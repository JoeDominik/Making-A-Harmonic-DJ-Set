import os
import sys
import spotipy
import copy
import random
import pandas as pd
import spotipy.util as util


#get the username from terminal
username = sys.argv[1]

#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

#create spotify object
spotify = spotipy.Spotify(auth=token)

user = spotify.current_user()

displayName = user['display_name']

while True:
    print()
    print("Welcome to Spotify " + displayName + ".")
    print()
    print("This is a tool to help you build a harmonic set from your desired playlist.")
    print("Enter 0 to make a harmonic set from one of your playlists.")
    print("Enter 1 if you would like to exit.")
    choice = input("Your choice: ")

    #Search for playlist 
    if choice == "0":
        print()
        playlist_id = input("Ok, what is the playlist URI? ")
        print()

        camelot_scores = {
        (0,1):'8B',
        (1,1):'3B',
        (2,1):'10B',
        (3,1):'5B',
        (4,1):'12B',
        (5,1):'7B',
        (6,1):'2B',
        (7,1):'9B',
        (8,1):'4B',
        (9,1):'11B',
        (10,1):'6B',
        (11,1):'1B',
        (0,0):'5A',
        (1,0):'12A',
        (2,0):'7A',
        (3,0):'2A',
        (4,0):'9A',
        (5,0):'4A',
        (6,0):'11A',
        (7,0):'6A',
        (8,0):'1A',
        (9,0):'8A',
        (10,0):'3A',
        (11,0):'10A',
        }
        def camelot_function(key, mode):
            return camelot_scores.get((key, mode))
        
        #get tracks of playlist
        results = spotify.user_playlist_tracks(user = user, playlist_id = playlist_id)
        tracks = results['items']
        while results['next']:
            results = spotify.next(results)
            tracks.extend(results['items'])
        #creating list for the music playlist
        playlist_dict = {
        '1A': [],
        '2A': [],
        '3A': [],
        '4A': [],
        '5A': [],
        '6A': [],
        '7A': [],
        '8A': [],
        '9A': [],
        '10A': [],
        '11A': [],
        '12A': [],
        '1B': [],
        '2B': [],
        '3B': [],
        '4B': [],
        '5B': [],
        '6B': [],
        '7B': [],
        '8B': [],
        '9B': [],
        '10B': [],
        '11B': [],
        '12B': [],
        }
        
        playlist_list = []
        for track in tracks:
            #getting the audio features for each track
            audio_features = spotify.audio_features(track['track']['id'])
            #appending to the list the track name, artist, popularity, tempo, key, danceability, energy, and loudness
            playlist_list.append([track['track']['name'], track['track']['artists'][0]['name'], track['track']['popularity'], 
                       audio_features[0]['tempo'], audio_features[0]['key'], audio_features[0]['mode'], 
                       audio_features[0]['danceability'], 
                       audio_features[0]['energy'], audio_features[0]['loudness'], 
                       camelot_function(audio_features[0]['key'], audio_features[0]['mode'])])
            playlist_dict[camelot_function(audio_features[0]['key'], audio_features[0]['mode'])].append([track['track']['name'],
                        track['track']['artists'][0]['name'], track['track']['popularity'], 
                       audio_features[0]['tempo'], audio_features[0]['key'], audio_features[0]['mode'], 
                       audio_features[0]['danceability'], 
                       audio_features[0]['energy'], audio_features[0]['loudness'], 
                       camelot_function(audio_features[0]['key'], audio_features[0]['mode'])])
        #making the dataframe after done with the for loop
        song_df = pd.DataFrame(playlist_list, columns = ['Song Name', 'Artist', 'Popularity', 'Tempo', 'Key', 'Mode',
                                               'Danceability', 'Energy', 'Loudness', 'Camelot Score']) 
  

        harmony_dict = {
        '1A':['12A', '1A', '2A', '1B'],
        '2A':['1A', '2A', '3A', '2B'],
        '3A':['2A', '3A', '4A', '3B'],
        '4A':['3A', '4A', '5A', '4B'],
        '5A':['4A', '5A', '6A', '5B'],
        '6A':['5A', '6A', '7A', '6B'],
        '7A':['6A', '7A', '8A', '7B'],
        '8A':['7A', '8A', '9A', '8B'],
        '9A':['8A', '9A', '10A', '9B'],
        '10A':['9A', '10A', '11A', '10B'],
        '11A':['10A', '11A', '12A', '11B'],
        '12A':['11A', '12A', '1A', '12B'],
        '1B':['12B', '1B', '2B', '1A'],
        '2B':['1B', '2B', '3B', '2A'],
        '3B':['2B', '3B', '4B', '3A'],
        '4B':['3B', '4B', '5B', '4A'],
        '5B':['4B', '5B', '6B', '5A'],
        '6B':['5B', '6B', '7B', '6A'],
        '7B':['6B', '7B', '8B', '7A'],
        '8B':['7B', '8B', '9B', '8A'],
        '9B':['8B', '9B', '10B', '9A'],
        '10B':['9B', '10B', '11B', '10A'],
        '11B':['10B', '11B', '12B', '11A'],
        '12B':['11B', '12B', '1B', '12A'],
        }
        def harmony_function_2(score):
            return harmony_dict.get(score) 
    

        playlist_dict_2 = copy.deepcopy(playlist_dict)
        final_playlist_list = []
        #constructing the list for the songs that satisfy the constraints later in the program
        potential_song_list = []
        #starting the confirmation for the first song with N
        confirmation = "N"
        #this while loop goes until something other than N is put in (could still work on)
        while(confirmation == "N"):
            #asks the user for a number between the starting and ending index of the playlist
            starting_song_index = input("To start the set please enter a number between " + str(0) +
                                " and " + str(len(song_df) - 1) + " : ")
            starting_song_index = int(starting_song_index)
            #finds the song in the data frame and asks the user if this is the correct song
            starting_song = song_df.iloc[starting_song_index]
            print("Starting song for set: " + str(starting_song['Song Name']) + " by " + str(starting_song['Artist']))
            confirmation = input("Is this correct? Type Y for yes and N for no: ")
        #after finding the correct song, the tempo and camelot score of that song is found
        previous_song_camelot = starting_song['Camelot Score']
        previous_song_tempo = starting_song['Tempo']
        starting_song = starting_song.tolist()
        #the song is then removed from the value from the specific camelot score it was in
        value_from_specific_camelot = playlist_dict_2.pop(previous_song_camelot)
        value_from_specific_camelot.remove(starting_song)
        #the other songs that were not affected were put back into the dictionary
        playlist_dict_2[previous_song_camelot] = value_from_specific_camelot
        #the first song is then added to the final playlist
        final_playlist_list.append(starting_song)
        indicator = True
        #this while loop goes through the rest of the dictionary, adding to the final playlist if the constraints are met
        while((len(final_playlist_list) < len(song_df)) and (indicator == True)):
            #this finds all songs that are within the 4 camelot scores of the previous song
            corresponding_camelot_scores = harmony_function_2(previous_song_camelot)
            for camelot_score in corresponding_camelot_scores:
                songs = playlist_dict_2[camelot_score]
                for song in songs:
                    #this constraint makes sure no songs outside of 5 BPM are added to the list of potential songs
                    if(abs(song[3] - previous_song_tempo) < 5):
                        potential_song_list.append(song)
            #making sure the potential song list is not empty
            if(len(potential_song_list) > 0 ):
               #in order to keep randomness with the playlist, a random integer is generated
                random_int = random.randint(0,len(potential_song_list) - 1)
                #this next song is then found, the camelot score and tempo for that song are found
                next_song = potential_song_list[random_int]
                next_song_camelot = next_song[9]
                next_song_tempo = next_song[3]
                #the next song is then removed from the dictionary at the specific camelot score
                value_from_specific_camelot = playlist_dict_2.pop(next_song_camelot)
                value_from_specific_camelot.remove(next_song)
                playlist_dict_2[next_song_camelot] = value_from_specific_camelot
                #finally, the final playlist is added with the next song
                final_playlist_list.append(next_song)
                #the previous song camelot score and tempo are the next song camelot score and tempo, respectfully
                previous_song_camelot = next_song_camelot
                previous_song_tempo = next_song_tempo
                #to keep the potential song list empty, it is cleared
                potential_song_list.clear()
            else:
                indicator = False
        #the final playlist dataframe is constructed to make it easier to read
        playlist_df = pd.DataFrame(final_playlist_list, columns = ['Song Name', 'Artist', 'Popularity', 'Tempo', 'Key', 'Mode', 
                                                           'Danceability', 'Energy', 'Loudness', 'Camelot Score'])  
        #after, the playlist dataframe is printed to make sure it works
        print(playlist_df)
    #End program
    if choice == "1":
        break

