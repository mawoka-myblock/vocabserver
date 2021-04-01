from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
import requests
import config
from config import geturl
import json
from functools import partial


def login():
    login_fields = input_group("Bitte einloggen!",
                               [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                input("Dein Pasword", name="password", type="password"), ])

    response = requests.post(f'{geturl()}/auth/jwt/login', headers={'accept': 'application/json',
                                                                    'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'grant_type': '', 'username': f'{login_fields["mail"]}',
                                   'password': f'{login_fields["password"]}', 'scope': '', 'client_id': '',
                                   'client_secret': ''})
    with use_scope('First_Scope', clear=True):
        try:
            try:
                if "LOGIN_BAD_CREDENTIALS" == json.loads(response.text)["detail"]:
                    put_error("Falsche Anmeldedaten!")
                    login()

            except:
                if "bearer" == json.loads(response.text)["token_type"]:
                    token = json.loads(response.text)["access_token"]
                    put_success("Logged in succesfully!")
        except:
            put_text("Unknown Error!")


def create_vocab():
    select = input_group("Was möchtest du erstellen?", )


# start_server(login)
start_server([login], port=5000)
