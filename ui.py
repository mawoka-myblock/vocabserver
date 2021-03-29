from pywebio.input import *
from pywebio.output import *
import requests
import config

## Login Screen
def check_password(password):
    if len(password) <= config.passwdlength():
        return "Das Passwort muss falsch sein, da es unter 6 Zeichen lang ist!"


def login():
    login = input_group("Bitte einloggen!", [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                             input("Dein Pasword", name="password", type="password", validate=check_password)])