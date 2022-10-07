import pandas as pd
import random

def filtered_songs():
	all_songs = pd.read_csv("../data/songs.csv")
	all_songs = all_songs.filter(["title", "artist", "year", "top genre"])
	return all_songs

def get_all_songs():
	all_songs = pd.read_csv("../data/songs.csv")
	return all_songs 

def recommend(input_songs):
    # removing all songs with count = 1
    songs = get_all_songs()
    songs = songs.groupby('top genre').filter(lambda x : len(x)>0)
    # creating dictionary of song titles and genre
    playlist = dict(zip(songs['title'], songs['top genre']))
    # creating dictionary to count the frequency of each genre
    freq = {}
    for item in songs['top genre']:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    # create list of all songs from the input genre
    selected_list = []
    output = []
    for input in input_songs:
        if input in playlist.keys():
            for key, value in playlist.items():
                if playlist[input] == value:
                    selected_list.append(key)
            selected_list.remove(input)
    if (len(selected_list) >= 10):
        output = random.sample(selected_list, 10)
    else:
        extra_songs = 10 - len(selected_list)
        song_names = songs['title'].to_list()
        song_names_filtered = [x for x in song_names if x not in selected_list]
        selected_list.extend(random.sample(song_names_filtered, extra_songs))
        output = selected_list.copy()
    return output
