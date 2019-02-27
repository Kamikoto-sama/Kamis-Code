import speech_recognition as sr
import os
import sys
import webbrowser
import pyttsx3

count = 0


def talk(words):
    print(words)
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()


talk("Ну чо те")


def command():
    rec = sr.Recognizer()

    with sr.Microphone() as source:
        rec.pause_threshold = 1
        rec.adjust_for_ambient_noise(source, 1)
        audio = rec.listen(source)

    try:
        task = rec.recognize_google(audio, language='ru-RU').lower()
        print(">>>", task)
    except sr.UnknownValueError:
        talk("Вынь хуй изорта")
        task = command()

    return task


def execute(task):
    if 'открой' in task:
        talk("Лави ебать")
        webbrowser.open("http://natribu.org/")
    elif 'закройся' in task or 'нахуй' in task:
        talk("Ливаю нахой")
        sys.exit()
    elif 'скажи' in task:
        talk('Точно не ты')
    elif 'кто' in task:
        talk('это Макар Зарчуков')
    elif 'алло' in task:
        talk("Хуле надо")
    elif 'нет' in task:
        talk('Пидора ответ')
        talk('Хочешь анектод')
    elif 'здорово' in task or 'привет' in task:
        talk('здарова ебать')
    elif 'анекдот' in task:
        talk("Заходит даниил в бар. и")
        talk("и идет нахуй потому что бар для данилов ахах ахах")
    elif 'да' in task:
        talk('Пизда')
        talk("Заходит даниил в бар и")
        talk("и идет нахуй потому что бар для данилов ахах ахах")
    else:
        global count
        count += 1
        talk("Нихуя не поняла")
        if count == 3:
            talk('Хочешь анекдот?')

while True:
    execute(command())
