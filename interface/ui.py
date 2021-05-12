import json

import requests
from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *

from icecream import ic
import interface.create
import interface.dictonary
import interface.learn
from config import geturl


def convert_lang(word):
    if word == "Französisch":
        return "french"
    elif word == "Latein":
        return "latin"
    elif word == "Englisch":
        return "english"
    else:
        print("Unexpected error in interface.ui.convert_lang")
        return "error"





def select_what_to_do():
    what_to_do = input_group("Was möchtest du machen?", [select('Was möchtest Du machen?', ['Lernen', "Erstellen", "Wörterbuch"], name="action"), select("Welche Sprache?", ['Englisch', "Französisch", "Latein"], name="language")])
    if what_to_do["action"] == "Lernen":
        interface.learn.index(convert_lang(what_to_do["language"]), classroom)
    elif what_to_do["action"] == "Erstellen":
        interface.create.index(convert_lang(what_to_do["language"]), token, classroom)                                 #convert_lang(what_to_do["language"])
    elif what_to_do["action"] == "Wörterbuch":
        interface.dictonary.index(convert_lang(what_to_do["language"]))


def login():
    login_fields = input_group("Bitte einloggen!",
                               [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                input("Dein Pasword", name="password", type="password"),
                                input("Deinen Klassenraum", name="classroom")])
    global classroom
    if len(login_fields["classroom"]) == 1:
        classroom = "00" + login_fields["classroom"]
    elif len(login_fields["classroom"]) == 2:
        classroom = "0" + login_fields["classroom"]
    elif len(login_fields["classroom"]) == 3:
        classroom = login_fields["classroom"]
    else:
        print("Unexpected error in interface.ui.login!")
    response = requests.post(f'{geturl()}/api/v1/auth/jwt/login', headers={'accept': 'application/x-www-form-urlencoded',
                                                                    'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'grant_type': '', 'username': f'{login_fields["mail"]}',
                                   'password': f'{login_fields["password"]}', 'scope': '', 'client_id': '',
                                   'client_secret': ''})
    with use_scope('First_Scope', clear=True):
        try:
            if "LOGIN_BAD_CREDENTIALS" == json.loads(response.text)["detail"]:
                put_error("Falsche Anmeldedaten!")
                login()

        except:
            if "bearer" == json.loads(response.text)["token_type"]:
                global token
                token = json.loads(response.text)["access_token"]
                put_success("Logged in succesfully!")
                select_what_to_do()


# start_server(login)
#start_server([login], port=5000)
