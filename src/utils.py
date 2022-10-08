from youtubesearchpython import VideosSearch

from get_all import filtered_songs


def searchSong(name_song):
    print(name_song)
    videosSearch = VideosSearch(name_song, limit=1)
    result = videosSearch.result()
    link = result['result'][0]['link']
    return link


all_songs = filtered_songs()[["title", "artist", "top genre"]]


def random_ten():
    ten_random_songs = (all_songs.sample(
        frac=1).groupby('top genre').head(1)).sample(10)
    return ten_random_songs
