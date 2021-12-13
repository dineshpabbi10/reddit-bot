import os
from mutagen.mp3 import MP3
from pydub import AudioSegment

def getCwd():
    return os.getcwd()

def createFolder(root,name):
    if not os.path.exists(os.path.join(root,name)):
        os.makedirs(os.path.join(root,name))

def getAudioLength(path,addition):
    audio = MP3(path)
    audioTime = audio.info.length
    audioTime = round(audioTime,1)+addition
    return audioTime

def cleanDirectory(fileName):
    path = os.path.join(getCwd(),"export")
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
    os.remove(os.path.join(getCwd(),fileName+".avi"))
    os.remove(os.path.join(getCwd(),fileName+".mp3"))

def combineAudio(audioFile,path):
    audioFile = audioFile + AudioSegment.from_mp3(path)
    return audioFile
