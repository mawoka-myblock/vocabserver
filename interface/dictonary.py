from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
import requests
import config
from config import geturl
import json
from functools import partial
import interface.ui as ui

def index(language):
    with use_scope("First_Scope", clear=True):
        put_error("Noch nicht nutzbar!")
        ui.select_what_to_do()