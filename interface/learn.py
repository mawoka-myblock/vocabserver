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
    response = requests.get(f'{geturl()}/api/vocab/read-list/{subject}/{classroom}/{id}', headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    vocab_undone = json.loads(response.text)
    vocab = random.sample(vocab_undone.items(), k=len(vocab_undone))
    return dict(vocab)


def getstats(subject):
    response = requests.get(f'{geturl()}/api/students/get-stats/{subject}/', headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})


def index(subject, classroom):

    response = requests.get(f'{geturl()}/api/vocab/list-list/{subject}/{classroom}', headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})

    with use_scope('First_Scope', clear=True):
        what_to_do = input("Bitte wähle das Kapitel aus!", datalist=json.loads(response.text))
        vocab = getvocab(classroom, subject, what_to_do)
        put_text(vocab)
        for i in vocab:
            input_group(f"Please enter the {subject} word!",[put_text(vocab.key[1]), input(f"Input the {subject} word", name="word")])









