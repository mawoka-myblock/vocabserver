from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
from config import geturl
import ui
import requests
import json

lang1List = []
lang2List = []


# answer = radio("Please Choose A Language", options=['English','French'])

def index(language, token):
    with use_scope("First_Scope", clear=True):
        Words = input_group("Some text", [input("Please Enter The German Word：", name="Lang1", required=True),
                                          input("Please Enter The Translation：", name="Lang2", required=True),
                                          checkbox(options=["Go on!"])])  # TODO: is a huge problem!

        #go_on = checkbox("I'm Done!")
        lang1List.insert(len(lang1List), Words["Lang1"])
        lang2List.insert(len(lang2List), Words["Lang2"])

    answer = radio("Add More?", options=['Yes', 'No'])

    if answer == "No":
        put_text("German: ", lang1List)
        put_text("Put The Language Name Here: ", lang2List)
        pass
    else:
        index()


