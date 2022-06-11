import speech_recognition as sr
import os
from fuzzywuzzy import fuzz
import pyttsx3
import datetime


library = {
    "name": (
        'дельта', 'дельточка', 'дельтка', 'дольто'
    ),
    "rm": (
        'скажи', 'покажи', 'расскажи', 'сколько'
    ),
    "commands": {
        "time": ('сейчас времени', 'время', 'который час', 'часов', 'сейчас часов'),
        "date": ('какой сегодня день', 'какой день недели', 'какое сегодня число', 'какой сегодня день', 'дату'),
        "humor": ('анекдот', 'шутку', 'рассмеши меня', 'мне грустно', 'ты знаешь шутки?', 'ты знаешь анекдоты?'),
        "facts": ('интересный факт', 'факт'),
        "music": ('воспроизведи радио', 'включи радио', 'включи песни', 'включи музыку'),
        "repeat": ('повтори', 'повтори фразу', 'фразу', 'повтори за мной', 'повтори за мной фразу'),
    }
}


def speak(speech):
    pass
def listen_speech():
    pass
def processing(command):
    pass
def coincable(cmd):
    pass
def execute_cmd(cmd):
    pass

while True:
    pass