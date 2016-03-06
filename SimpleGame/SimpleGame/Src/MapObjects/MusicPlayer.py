from Utils.MapObjectBase import MapObjectBase, TiledObjectItem
from Utils.UserEvents import *
import Utils.DirHelper
import pygame
import os

class PlayerProps():
    Loop = "Loop"
    Start = "Start"

class MusicPlayer(MapObjectBase):
    """Implements the music player as map object."""

    SoundDictionary = {}
    SongDictionary = {}

    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(EVENT_MUSIC_ENDED)
        self._songs = []
        self._loop = None
        self._stop = False
        self._pause = False

    def configure(self, configuration):
        print(configuration)
        assert isinstance(configuration, TiledObjectItem), "Expected configuration of type TiledObjectItem."
        self.configureProperties(configuration.properties)
        return super().configure(configuration)

    def initializeObject(self, parent):
        super().initializeObject(parent)
        if self._start:
            self.play()

    def configureProperties(self, properties):
        """Configure the properties from TMX properties."""
        trueStringList = ['True', 'true', '1', 1]
        songlist = []

        for prop in properties:
            if prop == PlayerProps.Loop:
                self._loop = properties[prop] in trueStringList
            elif prop == PlayerProps.Start:
                self._start = properties[prop] in trueStringList
            else:
               song = {"Name" : prop, "FileName" : properties[prop]}
               self._songs.append(song)
               
         

    def loadSounds(self, soundConfig):
        for sound in soundConfig:
            resourceFileName = Utils.DirHelper.getSongResourceFile(sound["FileName"])
            if os.path.isfile(resourceFileName):
                #load file
                soundResource = pygame.mixer.Sound(resourceFileName)
                MusicPlayer.SoundDictionary[sound["Name"]] = soundResource
            else:
                logging.error("Song file missing: {0}".format(resourceFileName))
        pass

    def playSoundByName(self, soundname):
        if MusicPlayer.SoundDictionary[soundname]:
            MusicPlayer.SoundDictionary[soundname].play()
        else:
            logging.error("Sound not found: {0}".format(soundname))
        pass

    def play(self, index = 0):
        """Plays the song index."""
        if index != None:
            if len(self._songs) > 0:
                musicFile = Utils.DirHelper.getSongResourceFile(self._songs[index]["FileName"])
                if os.path.isfile(musicFile):
                    pygame.mixer.music.load(musicFile)
                    print("Playing song: ", self._songs[index]["FileName"])
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

    


