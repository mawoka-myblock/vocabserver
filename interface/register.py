from config import sentry, passwdlength
sentry()
from icecream import ic
from config import geturl, getdb
from contextlib import suppress
import requests
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import random
import re
import string
import json

def check_passwd_length(passwd):
    if len(passwd) < int(passwdlength()):
        return "Password too short"

def check_mail(mail):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return "Keine echte Mail-Adresse angegeben"


def random_str():
    random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))
    return random_string

def register():
    register_fields = input_group("Registrierung",
                                  [input("Deine E-Mail-Adresse", name="email", placeholder="hans@wurst.com", required=True, validate=check_mail),
                                   input("Dein Passwort", name="password", validate=check_passwd_length, placeholder=random_str(), required=True)])

    response = requests.post("http://127.0.0.1:8000/api/v1/auth/request-verify-token",
                      data='{"email": "%s"}' % register_fields["email"].replace("%40", "@"))
    print(response.text)
    r = requests.post("http://127.0.0.1:8000/api/v1/auth/verify", data='{"token": "%s"}' % response.json["token"])
