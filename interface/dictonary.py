from config import sentry
sentry()
from pywebio.output import *
import interface.ui as ui

def index(language):
    with use_scope("First_Scope", clear=True):
        put_error("Noch nicht nutzbar!")
        ui.select_what_to_do()