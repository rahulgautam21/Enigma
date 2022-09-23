import pandas as pd


#add pagination support
def get_all_songs(self):
	all_songs = pd.read_csv("../data/songs.csv")
	print(' Data has (rows, columns):', all_songs.shape)

	all_songs = all_songs.filter(["title", "artist", "year"])
	print(all_songs.head(10))
	return all_songs


