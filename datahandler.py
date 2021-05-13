import os
from contextlib import suppress

global response
from config import getdatadir, getdb
import json
import codecs
from icecream import ic
from cloudant.client import CouchDB


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
    for i in db:
        liste.append(i)
    return liste

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
            savetoindex(classroom, id, subject)
            return "Success"
    except Exception:
        return ic()
