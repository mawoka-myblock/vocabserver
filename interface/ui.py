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
import interface.create
import interface.dictonary
import interface.learn
from config import geturl, getdb
global email, password
from cryptography.fernet import Fernet

token = None

def login():
    put_html('<script async defer data-website-id="f2b2e6b6-d1e6-44f9-9023-8e64e264d818" src="https://analytics.mawoka.eu.org/umami.js"></script>')
    global token
    login_id = eval_js("localStorage.getItem('login_id')")
    if login_id is None:
        login_fields = input_group("Bitte einloggen!",
                                   [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com", required=True),
                                    input("Dein Paswort", name="password", type="password", required=True),
                                    input("Deinen Klassenraum", name="classroom", validate=check_classlevel, required=True),
                                    checkbox("Eingeloggt bleiben?", ["Ja"], name="stayloggedin")])

        response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                                 headers={'accept': 'application/x-www-form-urlencoded',
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': '', 'username': login_fields["mail"],
                                       'password': login_fields["password"], 'scope': '', 'client_id': '',
                                       'client_secret': ''})

        with use_scope('First_Scope', clear=True):
            put_html('<script async defer data-website-id="f2b2e6b6-d1e6-44f9-9023-8e64e264d818" src="https://analytics.mawoka.eu.org/umami.js"></script>')
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
                    token = json.loads(response.text)["access_token"]

                    put_success("Logged in succesfully!")
                if login_fields["stayloggedin"]:
                    key = Fernet.generate_key()
                    run_js("localStorage.setItem('encryption_key', key);", key=key.decode("ascii"))
                    classlevel = login_fields["classroom"]
                    if classlevel == "5":
                        cl = "five"
                    elif classlevel == "6":
                        cl = "six"
                    elif classlevel == "7":
                        cl = "seven"
                    elif classlevel == "8":
                        cl = "eight"
                    run_js("localStorage.setItem('classlevel', level)", level=cl)
                    random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
                    run_js("localStorage.setItem('login_id', id);", id=random_string)
                    cipher_suite = Fernet(key)
                    password = cipher_suite.encrypt(login_fields["password"].encode("ascii"))
                    email = cipher_suite.encrypt(login_fields["mail"].encode("ascii"))
                    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
                    db = client["sli"]
                    db.create_document({"_id": ":".join(("logged_in", random_string)), "password": password.decode("ascii"), "email": email.decode("ascii")})
                    client.disconnect()

                else:
                    put_error("Unknown error!")
                    capture_message('Something went wrong')
        select_what_to_do()
    else:
        encryption_key = eval_js("localStorage.getItem('encryption_key')")
        global classroom
        classroom = eval_js("localStorage.getItem('classlevel')")
        client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
        db = client["sli"]
        doc = db[":".join(("logged_in", login_id))]
        del doc["_id"]
        del doc["_rev"]
        key = encryption_key.encode("ascii")
        cipher_suite = Fernet(key)
        password = cipher_suite.decrypt(doc["password"].encode("ascii")).decode()
        email = cipher_suite.decrypt(doc["email"].encode("ascii")).decode()
        client.disconnect()
        response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                                 headers={'accept': 'application/x-www-form-urlencoded',
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': '', 'username': email,
                                       'password': password, 'scope': '', 'client_id': '',
                                       'client_secret': ''})
        with use_scope('First_Scope', clear=True):
            put_html('<script async defer data-website-id="f2b2e6b6-d1e6-44f9-9023-8e64e264d818" src="https://analytics.mawoka.eu.org/umami.js"></script>')
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

                    token = json.loads(response.text)["access_token"]

                    put_success("Logged in succesfully!")
        select_what_to_do()








def getuserdata(email, password):
    email = email
    password = password


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
                              select("Welche Sprache?", ['Englisch', "Französisch", "Latein"], name="language"),
                              checkbox("Ausloggen?", ["Ja"], name="logout")])
    if what_to_do["logout"]:
        client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
        login_id = eval_js("localStorage.getItem('login_id')")
        db = client["sli"]
        doc = db[f"logged_in:{login_id}"]
        doc.delete()
        doc.save()
        client.disconnect()
        run_js('localStorage.removeItem("login_id")')
        run_js('localStorage.removeItem("encryption_key")')
        run_js('localStorage.removeItem("classlevel")')
        run_js("location.reload()")



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



