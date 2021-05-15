import sentry_sdk
sentry_sdk.init(environment="development")
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
import asyncio
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
from time import sleep

def getuserdata(email, password):
    #register_thread()
    email = email
    password = password
    ic(email, password)



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


async def select_what_to_do():
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
        client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
        db = client["userdata"]
        #javascript = run_js("""(function(){
        #var loginid = localStorage.getItem('login_id');
        #console.log(loginid);
        #console.log(lol);
        #return loginid;
        #});
        #""", lol="HALLO")
        #print(javascript)
        #run_js("console.log('HALLO')")
        #current_url = eval_js("window.location.href")

        js = run_js('''(function(){
            var loginid = localStorage.getItem('login_id');
            rqcontent = "loginid=" + loginid;
            url = url + "?loginid=" + loginid;
            console.log(rqcontent)
            request = {};
            console.log(loginid, url);
            request = new XMLHttpRequest();
            request.open("POST", url, true);
            request.setRequestHeader("Content-Type", "application/json", "Access-Control-Allow-Origin:", "*");
            request.send();
            return rqcontent;
        })()''', url="http://127.0.0.1:8000/api/v1/auth/stay-signed-id")

        #put_text(eval_js("window.location.href"))
        sleep(1)
        email = local.email
        password = local.password
        put_text(local.email, local.password)
        response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                                 headers={'accept': 'application/x-www-form-urlencoded',
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': '', 'username': f'{email}',
                                       'password': f'{password}', 'scope': '', 'client_id': '',
                                       'client_secret': ''})
    try:
        ic(password, email)
        print(password, email)
        response = requests.post(f'{geturl()}/api/v1/auth/jwt/login',
                                 headers={'accept': 'application/x-www-form-urlencoded',
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={'grant_type': '', 'username': f'{email}',
                                       'password': f'{password}', 'scope': '', 'client_id': '',
                                       'client_secret': ''})
        put_text(response.text)
    except:
        ic()
        #put_text(function_res)
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
