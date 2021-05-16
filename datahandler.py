import sentry_sdk
sentry_sdk.init(environment="development")
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
#from cryptography.fernet import Fernet

import os
from contextlib import suppress
import re
global response
from config import getdatadir, getdb
import json
import codecs
from icecream import ic
from cloudant.client import CouchDB
import interface.ui as ui
import os
from auth import SECRET




def save(subject, classlevel, id, l1, l2):
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    if f"{subject}:{id}" in db:
        doc_save = db[f"{subject}:{id}"]
        document = doc_save
        document[l1] = l2
        document.save()
        del document
        return "Success"
    elif f"{subject}:{id}" not in db:
        db.create_document({"_id": ":".join((subject, id)), l1: l2})
        if f"{subject}:{id}" in db:
            return "Success"
        else:
            return "Couldn't create Document"
    client.disconnect()


def read(subject, classlevel, id):
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    doc = db[":".join((subject, id))]
    del doc["_id"]
    del doc["_rev"]
    return doc
    del doc
    client.disconnect()


def getcontent(subject, classlevel):
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    liste = []
    #re.findall()
    for i in db:
        liste.append(i["_id"])
    result = []
    print(liste)
    for i in liste:
        print(i)
        result.append(i.replace(f"{subject}:", ""))
    return result
    #return str(liste).replace(f"{subject}:", "")

# Will return overview about available chapters



def editcontent(subject, classlevel, id, lone, ltwo):
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    doc = db[":".join((subject, id))]
    doc[lone] = ltwo
    doc.save()
    client.disconnect()
    return "Success"


def filehandler(subject, classroom, id, file):
    try:
        with open(os.path.join(f'{getdatadir()}/vocab/{classroom}/{subject}/{id}.json'), "w") as f:
            file_decoded = codecs.decode(file, "UTF-8")
            ic(file_decoded)
            f.write(file_decoded)
            #savetoindex(classroom, id, subject)
            return "Success"
    except Exception:
        return ic()

def stayloggedin(loginid, id):
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client["userdata"]
    doc_save = db[f"stayin:{id}"]
    document = doc_save
    document["loginid"] = loginid
    document.save()
    del document, doc_save
    return "Success"
