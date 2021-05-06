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
    random.shuffle(german)
    random.shuffle(subject_word)


def getstats(subject):
    response = requests.get(f'{geturl()}/api/students/get-stats/{subject}/',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    return response.json()

@use_scope("First_scope")
def inputgroup(subject):
    for i in range(len(german)):
        input_group(f"Please enter the {subject} word!", [input(f"Input the {german[i]} word", name="word")])
        put_text(i)


def index(subject, classroom):
    response = requests.get(f'{geturl()}/api/vocab/list-list/{subject}/{classroom}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})

    with use_scope('First_Scope', clear=True):
        what_to_do = input("Bitte wähle das Kapitel aus!", datalist=json.loads(response.text))
        getvocab(classroom, subject, what_to_do)
        inputgroup(subject)



