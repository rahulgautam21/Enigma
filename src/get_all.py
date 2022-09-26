import pandas as pd

def filtered_songs():
	all_songs = pd.read_csv("../data/songs.csv")
	all_songs = all_songs.filter(["title", "artist", "year", "top genre"])
	return all_songs

def get_all_songs():
	all_songs = pd.read_csv("../data/songs.csv")
	return all_songs 


