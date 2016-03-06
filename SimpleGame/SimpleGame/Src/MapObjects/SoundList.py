from Utils.MapObjectBase import MapObjectBase, TiledObjectItem
import Utils.DirHelper
import logging
import os.path
import pygame


class SoundList(MapObjectBase):
    """Loads the sound resources into the sound dictionary and plays the sounds by name"""

    SoundDictionary = {}

    def __init__(self):
        return super().__init__()

    def configure(self, configuration):
        assert isinstance(configuration, TiledObjectItem), "Expected configuration of type TiledObjectItem."
        self.configureProperties(configuration.properties)
        return super().configure(configuration)

    def initializeObject(self, parent):
        parent.soundPlayer = self
        return super().initializeObject(parent)

    def configureProperties(self, properties):
        sounds = []
        for sndName in properties:
            resource = {"Name": sndName, "FileName" : properties[sndName]}
            sounds.append(resource)

        self.loadSounds(sounds)
        pass

    def loadSounds(self, soundConfig):
        for sound in soundConfig:
            resourceFileName = Utils.DirHelper.getSongResourceFile(sound["FileName"])
            if os.path.isfile(resourceFileName):
                #load file
                soundResource = pygame.mixer.Sound(resourceFileName)
                SoundList.SoundDictionary[sound["Name"]] = soundResource
            else:
                logging.error("Song file missing: {0}".format(resourceFileName))
        pass

    def playSoundByName(self, soundname):
        if SoundList.SoundDictionary[soundname]:
            SoundList.SoundDictionary[soundname].play()
        else:
            logging.error("Sound not found: {0}".format(soundname))
        pass


