import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyowm
from pyowm.utils.config import get_default_config

library2 = {
    "yes": ('да', 'да пожалуйста', 'конечно', 'естественно', 'давай', 'скажи', 'расскажи', 'говори'),
    "no": ('нет', 'не', 'не нужно', 'не надо', 'нет спасибо', 'спасибо но нет')
}
# Функция воспроизведения речи
def speak(speech):
    engine = pyttsx3.init()
    engine.say(speech)
    engine.runAndWait()
    engine.stop()


# Функция возращения записанной речи
def listen_speech():
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = ''
            command = ''
            audio = r.listen(source)
            command = r.recognize_google(audio, language="ru-RU").lower()
            return command
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        speak("Проверьте наличие интернета")

def final(detailed = {"wind": '', "humidity": '', "sky": ''}):
    speak("Рассказать подробней?")
    choise = listen_speech()
    percent = 0
    yn = ''
    for case, v in library2.items():
        for x in v:
            percent = fuzz.ratio(choise, x)
            if percent >= 50:
                yn = case
    print(yn)
    if yn == "yes":
        speak(detailed[0])
        speak(detailed[1])
        speak(detailed[2])
    elif yn == "no":    speak("Хорошо")
    else:
        speak("Не поняла, повторите пожалуйста")
        final(detailed)

def weath(place):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = pyowm.OWM('5c2110f38768c7df8d2a032f5519d9cd', config_dict)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    default = "В " + place + " сейчас " + w.detailed_status + ", температура на данный момент " + str(temp) + " градусов"
    detailed = {"wind": '', "humidity": '', "sky": ''}
    if w.wind()['speed'] <= 3.3:
        detailed[0] = "Ветра нет"
    elif w.wind()['speed'] <= 5.4:
        detailed[0] = "Ветер слабый, листья и тонкие ветви деревьев всё время колышутся. Скорость ветра " + str(w.wind()['speed']) + " метров за секунду"
    elif w.wind()['speed'] <= 7.9:
        detailed[0] = "Ветер умеренный, поднимает пыль и бумажки, приводит в движение тонкие ветви деревьев. Скорость ветра  " + str(w.wind()['speed']) + " метров за секунду"
    elif w.wind()['speed'] <= 10.7:
        detailed[0] = "Ветер свежий, качаются тонкие стволы деревьев, на воде появляются волны с гребнями. Скорость ветра  " + str(w.wind()['speed']) + " метров за секунду"
    elif w.wind()['speed'] <= 13.8:
        detailed[0] = "Ветер сильный, качаются толстые сучья деревьев, гудят телеграфные провода. Скорость ветра  " + str(w.wind()['speed']) + " метров за секунду"
    else:
        detailed[0] = "Ветер крепкий, качаются стволы деревьев, идти против ветра трудно. Скорость ветра  " + str(w.wind()['speed']) + " метров за секунду"
    detailed[1] = "Влажность составляет " + str(w.humidity) +"%"
    detailed[2] = "Облачность составляет: " + str(w.clouds) + "%"
    speak(default)
    final(detailed)