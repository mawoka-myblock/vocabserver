import sentry_sdk
sentry_sdk.init(environment="development")
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
from pywebio.input import *
from pywebio.output import *
import requests
from config import geturl
import json
import interface.ui as ui
import random
from icecream import ic


def getvocab(classroom, subject, id):
    global subject_word
    global german
    response = requests.get(f'{geturl()}/api/v1/vocab/read-list/{subject}/{classroom}/{id}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    vocab_undone = json.loads(response.text)
    german = []
    subject_word = []
    for items in vocab_undone.items():
        german.append(items[0]), subject_word.append(items[1])
    seed = random.random()
    temporary = list(zip(german, subject_word))
    random.shuffle(temporary)

    german, subject_word = zip(*temporary)


def getstats(subject):
    response = requests.get(f'{geturl()}/api/v1/students/get-stats/{subject}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    if response.text == "File not available":
        return "fna"
    else:
        return response.json()


@use_scope("First_scope")
def inputgroup(subject):
    for i in range(len(german)):
        put_text(f"{german[i]} is the same as {subject_word[i]}")
        words_entered = input_group(f"Please enter the {subject} word!",
                                    [input(f"Input the {german[i]} word", name="word")])
        stats = getstats(subject)
        try:
            if words_entered["word"] == subject_word[i]:
                put_text("Richtig")
                put_text(stats[subject_word[i]])
                if int(stats[subject_word[i]]) > 0:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': int(stats[subject_word[i]]) - 1})
                    put_text(response.text)
                elif int(stats[subject_word[i]]) <= 0:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': 0})
                    put_text(response.text)
            else:
                put_text(
                    f"Falsch, richtig wäre {subject_word[i]} gewesen, aber du hast '{words_entered['word']}' eingegeben.")
                if int(stats[subject_word[i]]) <= 0:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': int(stats[subject_word[i]]) + 1})
                    put_text(response.text)
                elif int(stats[subject_word[i]]) >= 3:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': 0})
                    put_text(response.text)

        except:
            put_text(subject_word[i])
            response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                     headers={'Content-Type': 'application/x-www-form-urlencoded',
                                              'Authorization': f'Bearer {ui.token}'},
                                     data={'ltwo': subject_word[i], 'hdiw': '3'})

            put_text(response.text)



def index(subject, classroom):
    response = requests.get(f'{geturl()}/api/v1/vocab/list-list/{subject}/{classroom}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})

    with use_scope('First_Scope', clear=True):
        what_to_do = input("Bitte wähle das Kapitel aus!", datalist=json.loads(response.text))
        getvocab(classroom, subject, what_to_do)
        inputgroup(subject)
