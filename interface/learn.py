from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
import requests
import config
from config import geturl
import json
from functools import partial
import ui
import random
from icecream import ic


def getvocab(classroom, subject, id):
    global subject_word
    global german
    response = requests.get(f'{geturl()}/api/vocab/read-list/{subject}/{classroom}/{id}',
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
    response = requests.get(f'{geturl()}/api/students/get-stats/{subject}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    if response.text == "File not available":
        return "fna"
    else:
        return response.json()

@use_scope("First_scope")
def inputgroup(subject):
    for i in range(len(german)):
        put_text(f"{german[i]} is the same as {subject_word[i]}")
        words_entered = input_group(f"Please enter the {subject} word!", [input(f"Input the {german[i]} word", name="word")])
        try:
            stats = getstats(subject)
            stats = stats[subject_word(i)]
        except:
            pass
        if words_entered["word"] == subject_word[i]:
            put_text("Richtig")
        else:
            put_text(f"Falsch, richtig wäre {subject_word[i]} gewesen, aber du hast '{words_entered['word']}' eingegeben.")


def index(subject, classroom):
    response = requests.get(f'{geturl()}/api/vocab/list-list/{subject}/{classroom}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})

    with use_scope('First_Scope', clear=True):
        what_to_do = input("Bitte wähle das Kapitel aus!", datalist=json.loads(response.text))
        getvocab(classroom, subject, what_to_do)
        inputgroup(subject)



