import random
import getpass
import speech_recognition
import speech_recognition as sr
import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser
import playsound
from threading import Thread
from wakeup import wakeup
#                                   -------------БИБЛИОТЕКА-------------
library = {
    "name": (
        'дельта', 'дельточка', 'дельтка', 'дольто', 'delta'
    ),
    "rm": (
        'расскажи', 'скажи', 'покажи', 'сколько', 'пожалуйста', 'будь добра'
    ),
    "commands": {
        "time": ('сейчас времени', 'время', 'который час', 'часов', 'сейчас часов'),
        "repeat": ('повтори', 'повтори фразу', 'фразу', 'повтори за мной', 'повтори за мной фразу', 'за мной'),
        "facts": ('интересный факт', 'факт'),
        "date": ('дату', 'какой сегодня день', 'какое сегодня число', 'какой день недели'),
        "weather": ('погоду', 'погоду на сегодня', 'какая погода', 'какая сейчас погода'),
        "humor": ('шутку', 'расскажи шутку', 'расскажи анекдот', 'анекдот', 'развесели меня', 'мне грустно', 'рассмеши меня', 'ты знаешь шутки' 'ты знаешь анекдоты'),
        "find": ('найди', 'в интернете', 'загугли', 'заяндекси', 'заопери', 'найди в опере', 'найди в гугле', 'найди в яндексе', 'в гугле', 'в яндексе', 'в опере',
                 'забей', 'в гугл', 'в оперу', 'в яндекс'),
        "write": ('запиши', 'запиши заметку', 'сделай заметку', 'запомни', 'заметка', 'запиши в заметку', 'запиши в заметки', 'в заметки',
                  'заметку', 'заметки'),
        "wakeup": ('засеки', 'поставь', 'таймер', 'будильник', 'засеки', 'таймер', 'засеки', 'будильник')
    }
}

#                                   -------------ФУНКЦИИ-------------

# Функция воспроизведения речи
def speak(speech):
    engine.say(speech)
    engine.runAndWait()
    engine.stop()


# Функция возращения записанной речи
def listen_speech():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1) #слушаем уровнь шума
            audio = ''
            command = ''
            audio = r.listen(source) #записываем речь
            command = r.recognize_google(audio, language="ru-RU").lower() #превращаем речь в текст
            return command
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        speak("Проверьте наличие интернета")


# Обработка записанной речи
def processing(command):
    try:
        cmd = command
        if cmd.startswith(library["name"]):  # если фраза начинается с имени ассистента, то береём во внимание
            for x in library["name"]:  # удаляем имя и ненужные слова из комманды
                cmd = cmd.replace(x, "").strip()
            for x in library["rm"]:
                cmd = cmd.replace(x, "").strip()
            return cmd
        else:
            return False  # иначе игнорируем фразу
    except AttributeError:
        pass


# Функция сравнения
def coincable(cmd):
    exec = ''
    try:
        for trigger in library["commands"]['find']:  # Делаем исключение для поиска, если находим триггер для него,
            if trigger in cmd:
                return ["find", cmd]
        for trigger in library["commands"]['wakeup']:# Делаем исключение для заметки, если находим триггер для него,
            if trigger in cmd:
                return["wakeup", cmd]
        for trigger in library["commands"]['write']:# Делаем исключение для заметки, если находим триггер для него,
            if trigger in cmd:
                return["write", cmd]
        for trigger in library["commands"]['repeat']:  # Делаем исключение для повторения, если находим триггер для него,
            if trigger in cmd:  # то взоращаем фразу которую нужно повторить и тип комманды
                return ["repeat", cmd]
    except TypeError:
        pass
    for type, v in library["commands"].items():  # перебираем тип комманды
        for x in v:  # берём триггер из типа комманды
            coin = fuzz.ratio(cmd, x)  # здесь узнаём процент схожести фразы с триггером
            if coin >= 50:  # если схожесть больше 50% то возращаем тип комманды
                return [type]


#                   -------------------------ВЫПОЛНЕНИЕ КОММАНД-------------------------

def weekday(date):
    # date = datetime.datetime.now().weekday()
    if date == 0:
        date = "понедельник"
        return date
    elif date == 1:
        date = "вторник"
        return date
    elif date == 2:
        date = "среда"
        return date
    elif date == 3:
        date = "четверг"
        return date
    elif date == 4:
        date = "пятница"
        return date
    elif date == 5:
        date = "суббота"
        return date
    else:
        date = "воскресенье"
        return date

def found(quest):
    quest = quest.replace("+", "%2B")
    quest = quest.replace("слэш", "%2F")
    quest = quest.replace("равно", "%3D")
    quest = quest.replace("процентов", "%25")
    quest = quest.replace("процент", "%25")
    quest = quest.replace("слеш", "%2F")
    quest = quest.replace("slash", "%2F")
    quest = quest.replace("плюс", "%2B")
    quest = quest.replace("plus", "%2B")
    quest = quest.replace("/", "%2F")
    return(quest)

# Функция выполнения комманды
def execute_cmd(type, proc_command):
    # ничего сложного, просто перебираем тип комманды и выполняем задачу
    # print(type) # debug
    try:
        if type[0] == "time":  # если тип комманды время
            # speak("Тайга сказала время") # debug
            time = ''
            time = datetime.datetime.now()  # записываем текущее время
            # print(time) # debug
            speak("Сейчас " + str(time.hour) + ":" + str(time.minute))  # говорим то что нам нужно
        elif type[0] == "date": # если тип комманды дата
            date = datetime.datetime.now()  # записывем нынешнюю дату
            # speak("Сегодня " + str(date.day) + " число " + str(date.month) + " месяц " + str(date.year) + " год") # debug
            day = weekday(date.weekday())  # вызываем функцию и узнаём какой день недели
            speak("Сегодня " + str(date.day) + "." + str(date.month) + "." + str(date.year) + ", " + day)
        elif type[0] == "repeat": # тип комманды повторение
            # speak("повтори")
            # print(command) # debug
            repeat = type[1] # берём из переменной второе значение
            for x in library["commands"]['repeat']:  # удаляем имя и ненужные слова из комманды
                repeat = repeat.replace(x, "").strip()
            speak("Хорошо, " + repeat)
        elif type[0] == "facts": # факты
            i = 0
            a = 0
            facts = ''
            #while i == 0:
            #    if a % 2 == 0:#именно факт а не "." находится в каждой второй строчке
            #        random.seed(version=2) #запускаем рандомайзер
            #        a = random.randint(0, 199) #берём рандомное число
            #    else:
            #        i += 1
            f = open('123.txt', "r", encoding="utf8") # открываем файл с фактами
            fact = f.read().split('\n')[a] #разделяем его по строкам и читаем нужную
            f.close()
            # print(fact) # debug
            speak("Интерестный факт, " + fact)
        elif type[0] == "weather":
            from weather import weath
            weath(place)
            pass
        elif type[0] == "find":
            for x in library["commands"]['find']:  # удаляем ненужные слова из комманды
                type[1] = type[1].replace(x, "")
            quest = found(type[1]) #функция заменит нужные символы на индексируемые
            quest = quest.strip() #чищем от ненужных пропусков
            #print(quest) #debug
            #print("\n" + type[1]) #debug
            speak("Хорошо, уже ищу")
            webbrowser.open('https://www.google.com/search?q=' + quest, new = 1) #открываем ссылку
        elif type[0] == "write":
            write = ''
            write = type[1]
            for x in library["commands"]['write']:  # удаляем ненужные слова из комманды
                write = write.replace(x, "")
            #print("\n [source] " + write)
            write = write.strip() # очищаем от ненужных пробелов
            #print("\n [right] " + write)
            speak("Записываю, " + write)
            a = "C:/Users/" + getpass.getuser() + "/Desktop/Заметка.txt" #получаем имя текущего пользователя
            file = open(a, 'a') #открываем файл
            file.write(write + '\n') #записываем
            file.close()
            speak("Записала")
        elif type[0] == "wakeup":
            try:
                hm = type[1]
                for x in library["commands"]['wakeup']:  # удаляем ненужные слова из комманды
                    hm = hm.replace(x, "").strip()
                print(hm)
                hm = int(hm)
                Thread(target=wakeup, args=("", hm)).start()
            except ValueError:
                speak("Не поняла, повторите ещё раз")
        else:
            speak("Я не знаю такой комманды")
    except TypeError:
        pass

#                               -------------ГЛАВНАЯ ФУНКЦИЯ-------------

# Запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
engine = pyttsx3.init()
speak("Добрый день!")
speak("Жду указаний...")
# Тело ассистента
while True:
    type = ''
    command = ''
    proc_command = ''
    place = 'Житомир, Украина'
    try:
        command = listen_speech()  # слушаем фразу
        print("[original command] " + command) # debug
        proc_command = processing(command)  # обрабатываем
        print("[proc_command] " + str(proc_command)) # debug
        if proc_command == False:  # если фраза не для ассистента --> пропускаем
            pass
        else:
            type = {"type": '', "rep": ''}
            type = coincable(proc_command)  # ищем тип комманды и выполняем её
            # print("[type] " + str(type)) # debug
            if type == None:  # если тип неизвестен
                speak("Я не знаю такой комманды")
            else:
                execute_cmd(type, proc_command)  # если же известный, то выполняем
    except TypeError:
        pass