from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
from config import geturl



import requests
import json

lang1List = []
lang2List = []

def index(language, token, classroom):
    with use_scope("First_Scope", clear=True):
        global id
        id = input("Please enter the Unit-ID", required=True)
    vocabhandler(language, token, classroom)


def vocabhandler(language, token, classroom):

    with use_scope('First_Scope', clear=True):
        Words = input_group("Bitte ausfüllen", [input("Please Enter The German Word：", name="Lang1", required=True),
                                          input("Please Enter The Translation：", name="Lang2", required=True),
                                          checkbox(name="done", options=["Done!"])])  # TODO: is a huge problem!

        lang1List.insert(len(lang1List), Words["Lang1"])
        lang2List.insert(len(lang2List), Words["Lang2"])


        if Words["done"]:
            dict(zip(lang1List, lang2List))
            put_text("German: ", lang1List)
            put_text("Put The Language Name Here: ", lang2List)
            put_table([
                ['German', "Other language"],
                {dict}
                ])
            confirm = actions("Confirm?", buttons=["Submit", "Cancel"])
            if confirm == "Submit":
                length = len(lang1List)
                for i in range(0, length):
                    r = requests.post(f'{geturl()}/api/vocab/add-list/{language}/{classroom}/{id}', headers={'accept': 'application/x-www-form-urlencoded', 'Authorization': f'Bearer {token}'}, data={"lone": lang1List[i], "ltwo": lang2List[i]})
                    print(r.text)
                    put_text(r.text)

            else:
                put_text("LOL")
        else:
            vocabhandler(language, token, classroom)






"""import random

my_dict = {"Hallo": "Hello", "Junge": "boy", "Mädchen": "girl"}
my_items = random.sample(my_dict.items(), k=len(my_dict))

for key, value in my_items:
    print(key, value)
    
"""
