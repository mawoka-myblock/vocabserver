import sentry_sdk
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
from pywebio.input import *
from pywebio.output import *
from pywebio.platform import *
from config import geturl
from icecream import ic

import requests

lang1List = []
lang2List = []

def index(language, token, classroom):
    clear("First_Scope")
    with use_scope("First_Scope"):
        global id
        startgroup = input_group("Please enter the Unit-ID", [input("Bitte hier die ID eingeben", name="id", required=True), file_upload(accept=".json", max_size="2M", placeholder="Here you can upload a file instead of typing it in manually!", name="file")])
        id = startgroup["id"]
        #ic(startgroup["file"]["filename"])
        #ic(startgroup["file"]["content"])
        try:
            r = requests.post(f"{geturl()}/api/v1/vocab/upload/{language}/{classroom}/{id}", headers={'accept': 'application/json', 'Authorization': f'Bearer {token}', 'Content-Type': 'multipart/form-data'}, data=startgroup["file"]["content"])
            ic(r.text)
        except Exception:
            vocabhandler(language, token, classroom)
            with use_scope("First_Scope"):
                toast("Keine Datei wurde hochgeladen!")

   # vocabhandler(language, token, classroom)



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
                    r = requests.post(f'{geturl()}/api/v1/vocab/add-list/{language}/{classroom}/{id}', headers={'accept': 'application/x-www-form-urlencoded', 'Authorization': f'Bearer {token}'}, data={"lone": lang1List[i], "ltwo": lang2List[i]})
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
