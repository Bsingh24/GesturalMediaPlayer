import os

from playsound import playsound

#playsound("sounds/gunshot.mp3", False)
audio_file = os.path.dirname(__file__) + '/sounds/gunshot.mp3'
playsound(audio_file)