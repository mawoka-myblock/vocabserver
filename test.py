import pywebio

from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from icecream import ic
from cryptography.fernet import Fernet
import random
import string


def main():
    login_fields = input_group("Bitte einloggen!",
                               [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                input("Dein Pasword", name="password", type="password"),
                                input("Deinen Klassenraum", name="classroom"),
                                checkbox("Eingeloggt bleiben?", ["Ja"], name="stayloggedin")])
    key = Fernet.generate_key()
    # print(key)
    run_js("localStorage.setItem('encryption_key', key);", key=key.decode("ascii"))
    random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    run_js("localStorage.setItem('login_id', id);", id=random_string)
    ic()
    cipher_suite = Fernet(key)
    ic()
    password = cipher_suite.encrypt(login_fields["password"].encode("ascii"))
    email = cipher_suite.encrypt(login_fields["mail"].encode("ascii"))
    print(password.decode("ascii"), email.decode("ascii"))


if __name__ == '__main__':
    pywebio.start_server(main, port=8000, debug=True)