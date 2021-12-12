import os
from mutagen.mp3 import MP3
from pydub import AudioSegment

def getCwd():
    return os.getcwd()

def createFolder(root,name):
    if not os.path.exists(os.path.join(root,name)):
        os.makedirs(os.path.join(root,name))

def getAudioLength(path):
    audio = MP3(path)
    audioTime = audio.info.length
    audioTime = round(audioTime,1)+1
    return audioTime

def cleanDirectory():
    path = os.path.join(getCwd(),"export")
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))

def combineAudio(audioFile,path):
    audioFile = audioFile + AudioSegment.from_mp3(path)
    return audioFile
