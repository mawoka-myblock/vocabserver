from pywebio.input import *
from pywebio.output import *
import requests
import config
from config import geturl

## Login Screen
def check_password(password):
    if len(password) <= config.passwdlength():
        return "Das Passwort muss falsch sein, da es unter 6 Zeichen lang ist!"


def login():
    login_fields = input_group("Bitte einloggen!", [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                             input("Dein Pasword", name="password", type="password", validate=check_password),])

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': '',
        'username': 'mawol@protonmail.com',
        'password': 'LauundSteffen',
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }

    response = requests.post(f'{geturl()}/auth/jwt/login', headers=headers, data={'grant_type': '', 'username': 'mawol@protonmail.com', 'password': f'{login_fields["password"]}', 'scope': '', 'client_id': '', 'client_secret': ''})