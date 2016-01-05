import pygame
import Utils.DirHelper
from Utils.UserEvents import EVENT_MUSIC_ENDED
import os


class MusicPlayer(object):
    """Class to play music in sequence."""
    def __init__(self, songs, start = True, loop = True):
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(EVENT_MUSIC_ENDED)
        self._songs = songs
        self._loop = loop
        self._stop = False
        self._pause = False
        if len(self._songs) > 0:
            self._currentSongIndex = 0
            if start:
                self.play(self._currentSongIndex)
        else:
            self._currentSongIndex = None
        pass

    def play(self, index = None):
        """Plays the song index."""
        if index != None:
            musicFile = Utils.DirHelper.getSongResourceFile(self._songs[index]["Filename"])
            if os.path.isfile(musicFile):
                pygame.mixer.music.load(musicFile)
                print("Playing song: ", self._songs[index]["Filename"])
                pygame.mixer.music.play()
        pass

    def playNextSong(self):
        if self._songs and len(self._songs) > 0 and self._stop == False:
            if self._currentSongIndex + 1 < len(self._songs):
                self._currentSongIndex += 1
                self.play(self._currentSongIndex)
            else:
                if self._loop:
                    self._currentSongIndex = 0
                    self.play(self._currentSongIndex)

    def stop(self):
        self._stop = True
        pygame.mixer.music.stop()

    def togglePause(self):
        if self._pause:
            self._pause = False
            pygame.mixer.music.pause()
        else:
            self._pause = True
            pygame.mixer.music.unpause()
    pass










