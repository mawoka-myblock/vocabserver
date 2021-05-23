from config import sentry
sentry()
import json
from sentry_sdk import capture_message
from cloudant.client import CouchDB
from contextlib import suppress
import requests
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import random
import string
from icecream import ic
import interface.create
import interface.dictonary
import interface.learn
from config import geturl, getdb
global email, password
from cryptography.fernet import Fernet

def getuserdata(email, password):
    email = email
    password = password
    ic(email, password)


global token


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
    login_id = eval_js("localStorage.getItem('login_id')")
    if login_id is None:
        login_fields = input_group("Bitte einloggen!",
                                   [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                    input("Dein Pasword", name="password", type="password"),
                                    input("Deinen Klassenraum", name="classroom", validate=check_classlevel),
                                    checkbox("Eingeloggt bleiben?", ["Ja"], name="stayloggedin")])

        response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                                 headers={'accept': 'application/x-www-form-urlencoded',
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': '', 'username': login_fields["mail"],
                                       'password': login_fields["password"], 'scope': '', 'client_id': '',
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
                ic()
                if "bearer" == json.loads(response.text)["token_type"]:
                    global token
                    token = json.loads(response.text)["access_token"]
                    ic("Hallo")

                    put_success("Logged in succesfully!")
                if login_fields["stayloggedin"]:
                    ic()
                    key = Fernet.generate_key()
                    print(key)
                    run_js("localStorage.setItem('encryption_key', key);", key=key.decode("ascii"))
                    run_js("localStorage.setItem('classlevel', level)", level=login_fields["classroom"])
                    random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
                    run_js("localStorage.setItem('login_id', id);", id=random_string)
                    cipher_suite = Fernet(key)
                    password = cipher_suite.encrypt(login_fields["password"].encode("ascii"))
                    email = cipher_suite.encrypt(login_fields["mail"].encode("ascii"))
                    print(password, email)
                    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
                    db = client["userdata"]
                    db.create_document({"_id": ":".join(("logged_in", random_string)), "password": password.decode("ascii"), "email": email.decode("ascii")})
                    client.disconnect()

                else:
                    put_error("Unknown error!")
                    capture_message('Something went wrong')
            ic()
        select_what_to_do()
    else:
        encryption_key = eval_js("localStorage.getItem('encryption_key')")
        global classroom
        classroom = eval_js("localStorage.getItem('classlevel')")
        client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
        db = client["userdata"]
        doc = db[":".join(("logged_in", login_id))]
        del doc["_id"]
        del doc["_rev"]
        print(login_id)
        key = encryption_key.encode("ascii")
        print(key)
        cipher_suite = Fernet(key)
        password = cipher_suite.decrypt(doc["password"].encode("ascii")).decode()
        email = cipher_suite.decrypt(doc["email"].encode("ascii")).decode()
        print(email, password)
        client.disconnect()
        response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                                 headers={'accept': 'application/x-www-form-urlencoded',
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': '', 'username': email,
                                       'password': password, 'scope': '', 'client_id': '',
                                       'client_secret': ''})
        print(response.text)
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
                    print(token)
                    token = json.loads(response.text)["access_token"]
                    print(token)

                    put_success("Logged in succesfully!")
        select_what_to_do()

