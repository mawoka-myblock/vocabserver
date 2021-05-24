from pywebio.platform.fastapi import start_server
from pywebio.output import *
from pywebio.platform.fastapi import start_server
from pywebio.session import *


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
def main():
    login_fields = input_group("Bitte einloggen!",
                               [input("Deine E-Mail-Adresse", name="mail", placeholder="hans@wurst.com"),
                                input("Dein Pasword", name="password", type="password"),
                                input("Deinen Klassenraum", name="classroom", validate=check_classlevel),
                                checkbox("Eingeloggt bleiben?", ["Ja"], name="stayloggedin")])
    already_logged_in = actions("Already logged in?", ["Yes", "No"])
    if already_logged_in == "Yes":
        val = eval_js("localStorage.getItem('login_id')")
        put_text('login_id', val)
    else:
        print("lol")
    hold()


if __name__ == '__main__':
    start_server(main, port=8000, debug=True)