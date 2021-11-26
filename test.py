import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

def speak(t):
    tts = gTTS(text=t, lang='ko')
    tts.save('test.mp3')
    playsound.playsound('test.mp3', device=1)

speak('안녕들하신가')
