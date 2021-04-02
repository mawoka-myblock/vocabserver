from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
import requests
import config
from config import geturl
import json
from functools import partial
import ui


def index(language):
    with use_scope('First_Scope', clear=True):
        what_to_do = input_group()
