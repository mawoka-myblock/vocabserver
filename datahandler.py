import os
from contextlib import suppress

global response
from config import getdatadir, getdb
import json
import codecs
from icecream import ic
from cloudant.client import CouchDB

client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
global db


# db = client["vocab"]

def savetoindex(classroom, id, subject):
    try:
        try:
            with open(os.path.join(f'{getdatadir()}/vocab/{classroom}/{subject}/index.json'), "r") as f:
                index = json.load(f)
            index.append(id)
            with open(os.path.join(f'{getdatadir()}/vocab/{classroom}/{subject}/index.json'), "w") as f:
                index = list(dict.fromkeys(index))
                json.dump(index, f, indent=2)
            print("Success")
        except:
            index = [id]
            with open(os.path.join(f'{getdatadir()}/vocab/{classroom}/{subject}/index.json'), "w") as f:
                json.dump(index, f, indent=2)
            print("Success")
    except:
        print(ic())


def save(subject, classroom, id, l1, l2):
    db = client["seven"]
    if f"{subject}:{id}" in db:
        doc = db[f"{subject}:{id}"]
        doc[l1] = l2
        doc.save()
        return "Success"
    elif f"{subject}:{id}" not in db:
        db.create_document({"_id": ":".join((subject, id)), l1: l2})
        if f"{subject}:{id}" in db:
            return "Success"
        else:
            return "Couldn't create Document"


def read(subject, classroom, id):
    db = client["seven"]
    doc = db[":".join((subject, id))]
    del doc["_id"]
    del doc["_rev"]
    return doc


def getcontent(subject, classroom):
    pass


# TODO: NEU MACHEN!!!


def editcontent(subject, classroom, id, lone, ltwo):
    return "NEEDS TO BE DONE AFTER WRITING STH ELSE IN JSON!!!"


def filehandler(subject, classroom, id, file):
    try:
        with open(os.path.join(f'{getdatadir()}/vocab/{classroom}/{subject}/{id}.json'), "w") as f:
            file_decoded = codecs.decode(file, "UTF-8")
            ic(file_decoded)
            f.write(file_decoded)
            savetoindex(classroom, id, subject)
            return "Success"
    except Exception:
        return ic()
