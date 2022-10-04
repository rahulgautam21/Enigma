from youtubesearchpython import VideosSearch


def searchSong(name_song):
    print(name_song)
    videosSearch = VideosSearch(name_song, limit=1)
    result = videosSearch.result()
    link = result['result'][0]['link']
    return link
