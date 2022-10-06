# This queue will store all the recommendation of the songs

class Songs_Queue():
    def __init__(self, song_names):
        self.queue = song_names
        self.index = 0

    def next_song(self):
        print(self.queue)
        if (self.index == len(self.queue)):
            self.index = 0
        val = self.index
        self.index += 1
        return self.queue[val]

    def prev_song(self):
        self.index -= 1
        if (self.index <= 0):
            self.index = len(self.queue) - 1
        val = self.index
        return self.queue[val]

    def get_len(self):
        return len(self.queue)
