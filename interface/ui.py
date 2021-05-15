import sentry_sdk
sentry_sdk.init(environment="development")
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
import json
from sentry_sdk import capture_message

from contextlib import suppress
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
    what_to_do = input_group("Was möchtest du machen?",
                             [select('Was möchtest Du machen?', ['Lernen', "Erstellen", "Wörterbuch"], name="action"),
                              select("Welche Sprache?", ['Englisch', "Französisch", "Latein"], name="language")])
    if what_to_do["action"] == "Lernen":
        interface.learn.index(convert_lang(what_to_do["language"]), classroom)
    elif what_to_do["action"] == "Erstellen":
        interface.create.index(convert_lang(what_to_do["language"]), token,
                               classroom)  # convert_lang(what_to_do["language"])
    elif what_to_do["action"] == "Wörterbuch":
        interface.dictonary.index(convert_lang(what_to_do["language"]))


def check_classlevel(classlevel):
    global classroom
    if classlevel == "5":
        classroom = "five"
    elif classlevel == "6":
        classroom = "six"
    elif classlevel == "7":
        classroom = "seven"
    elif classlevel == "8":
        classroom = "eight"
    else:
        return "Please enter a classleve between 5 and 8."


def login():
    already_logged_in = actions("Already logged in?", ["Yes", "No"])
    if already_logged_in == "Yes":
        put_text("HALLO")
    login_fields = input_group("Bitte einloggen!",
                               [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                input("Dein Pasword", name="password", type="password"),
                                input("Deinen Klassenraum", name="classroom", validate=check_classlevel)])

    response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                             headers={'accept': 'application/x-www-form-urlencoded',
                                      'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'grant_type': '', 'username': f'{login_fields["mail"]}',
                                   'password': f'{login_fields["password"]}', 'scope': '', 'client_id': '',
                                   'client_secret': ''})

    with use_scope('First_Scope', clear=True):
        with suppress(Exception):
            if "LOGIN_BAD_CREDENTIALS" == json.loads(response.text)["detail"]:
                put_error("Falsche Anmeldedaten!")
                login()
            else:
                put_error("Unknown error!")
                capture_message('Something went wrong')

        with suppress(Exception):
            if "Unauthorized" == json.loads(response.text)["detail"]:
                put_error("Deine E-Mail-Adresse ist noch nicht Verifiziert!")
            else:
                put_error("Unknown error!")
                capture_message('Something went wrong')

        with suppress(Exception):
            if "bearer" == json.loads(response.text)["token_type"]:
                global token
                token = json.loads(response.text)["access_token"]
                put_success("Logged in succesfully!")
                print(token)
                select_what_to_do()
            else:
                put_error("Unknown error!")
                capture_message('Something went wrong')

# start_server(login)
# start_server([login], port=5000)
