from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
import requests
import config
from config import geturl
import json
from functools import partial
import ui


def getvocab(classroom, subject, id):
    response = requests.get(f'{geturl()}/api/vocab/read-list/{subject}/{classroom}/{id}', headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})

def getstats(subject):
    response = requests.get(f'{geturl()}/api/students/get-stats/{subject}/', headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})


def index(subject, classroom):

    response = requests.get(f'{geturl()}/api/vocab/list-list/{subject}/{classroom}', headers={ 'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})

    with use_scope('First_Scope', clear=True):
        what_to_do = input("Bitte wähle das Kapitel aus!", datalist=json.loads(response.text))









