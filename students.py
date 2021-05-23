from config import sentry
sentry()
import json
import os

global data
from config import getdatadir, getdb
from cloudant import CouchDB

client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)

def saveresult(uid, ltwo, hdiw, subject):
    print(uid)
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client["userdata"]
    if f"{uid}:{subject}" in db:
        doc_sr = db[f"{uid}:{subject}"]
        document_lol = doc_sr
        document_lol[ltwo] = hdiw
        document_lol.save()
        del document_lol
    elif f"{uid}:{subject}" not in db:
        uid = str(uid)
        db.create_document({"_id": ":".join((uid, subject)), ltwo: hdiw})
    return "Success or not"
    client.disconnect()

def readresult(uid, subject):
    client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client["userdata"]
    if f"{uid}:{subject}" in db:
        doc_rr = db[":".join((str(uid), subject))]
        document = doc_rr
        if "_id" in document:
            del document["_id"]
            del document["_rev"]
        return document
        client.disconnect()
    else:
        return "File not available"
    #elif f"{uid}:{subject}" not in db:
    #    db.create_document({"_id": ":".join((uid, subject))})




def delete(uid, subject):
    try:
        os.remove(f"{getdatadir()}/userdata/{uid}/{subject}.json")
        return "Success"
    except:
        return "Error"
