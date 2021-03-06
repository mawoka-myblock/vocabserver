from config import sentry
sentry()
from pywebio.input import *
from pywebio.output import *
import requests
from config import geturl
import json
import interface.ui as ui
import random


def getvocab(classroom, subject, id):
    global subject_word
    global german
    response = requests.get(f'{geturl()}/api/v1/vocab/read-list/{subject}/{classroom}/{id}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    vocab_undone = json.loads(response.text)
    german = []
    subject_word = []
    for items in vocab_undone.items():
        german.append(items[0]), subject_word.append(items[1])
    seed = random.random()
    temporary = list(zip(german, subject_word))
    random.shuffle(temporary)

    german, subject_word = zip(*temporary)


def getstats(subject):
    response = requests.get(f'{geturl()}/api/v1/students/get-stats/{subject}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    if response.text == "File not available":
        return "fna"
    else:
        return response.json()




@use_scope("First_scope")
def inputgroup(subject):
    put_html('<script async defer data-website-id="f2b2e6b6-d1e6-44f9-9023-8e64e264d818" src="https://analytics.mawoka.eu.org/umami.js"></script>')
    for i in range(len(german)):
        #put_text(f"{german[i]} is the same as {subject_word[i]}")
        words_entered = input_group(f"Please enter the {subject} word!",
                                    [input(f"Input the German word for {german[i]}!", name="word")])
        stats = getstats(subject)
        try:
            if words_entered["word"] == subject_word[i]:
                put_markdown(f'<p><a style="color: green;"><strong>Richtig!</strong>&nbsp;</a><span style="text-decoration: underline;">{subject_word[i]}</span> hat nun den Score&nbsp;<strong>{int(stats[subject_word[i]])}</strong>.</p>')
                if int(stats[subject_word[i]]) > 0:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': int(stats[subject_word[i]]) - 1})
                elif int(stats[subject_word[i]]) <= 0:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': 0})
            else:
                put_html(f'<p><a style="color: red;"><strong>Falsch!</strong></a> Richtig w??re <span style="text-decoration: underline;">{subject_word[i]}</span> gewesen, aber du hast <strong>{words_entered["word"]}</strong> eingegeben.</p>')
                if int(stats[subject_word[i]]) <= 0:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': int(stats[subject_word[i]]) + 1})
                    #put_text(response.text)
                elif int(stats[subject_word[i]]) >= 3:
                    response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Authorization': f'Bearer {ui.token}'},
                                             data={'ltwo': subject_word[i], 'hdiw': 0})
                    #put_text(response.text)

        except:
            #put_text(subject_word[i])
            response = requests.post(f'{geturl()}/api/v1/students/write-stats/{subject}',
                                     headers={'Content-Type': 'application/x-www-form-urlencoded',
                                              'Authorization': f'Bearer {ui.token}'},
                                     data={'ltwo': subject_word[i], 'hdiw': '3'})

            #put_text(response.text)


def index(subject, classroom):
    response = requests.get(f'{geturl()}/api/v1/vocab/list-list/{subject}/{classroom}',
                            headers={'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'})
    def validate_lektion(user_input):
        global done
        for i in json.loads(response.text):
            if i == user_input:
                done = True
                pass
        if not done:
            return "No entry from list"
        #print(ui.token, "Hallo")


    with use_scope('First_Scope', clear=True):
        put_html('<script async defer data-website-id="f2b2e6b6-d1e6-44f9-9023-8e64e264d818" src="https://analytics.mawoka.eu.org/umami.js"></script>')
        what_to_do = input("Bitte w??hle das Kapitel aus!", datalist=json.loads(response.text), validate=validate_lektion)
        getvocab(classroom, subject, what_to_do)
        inputgroup(subject)
