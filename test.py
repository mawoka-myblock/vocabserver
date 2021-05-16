import pywebio

from pywebio.input import *
from pywebio.output import *
from pywebio.session import *


def main():
    already_logged_in = actions("Already logged in?", ["Yes", "No"])
    if already_logged_in == "Yes":
        val = eval_js("localStorage.getItem('login_id')")
        put_text('login_id', val)

    hold()


if __name__ == '__main__':
    pywebio.start_server(main, port=8000, debug=True)