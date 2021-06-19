from config import sentry

sentry()
import os

global data
from config import getdatadir, getdb, get_db_name, get_db_connection_str
from pymongo import MongoClient
from contextlib import suppress
client = MongoClient(get_db_connection_str())




def saveresult(uid: str, ltwo: str, hdiw: int, subject: str) -> str:
    db = client[get_db_name()]
    """if f"{uid}:{subject}" in db.list_collection_names():
        post = {subject: {uid: {ltwo: hdiw}}}
        posts = db.posts
        posts.insert_one(post)

    elif f"{uid}:{subject}" not in db:
        uid = str(uid)
        db.create_document({"_id": ":".join((uid, subject)), ltwo: hdiw})
    client.disconnect()
    return "Success or not"""

    col = db["userdata"]
    #posts.update_one({subject} , post)
    if type(col.find_one({"_subject": subject, "_user": str(uid)})) == type(None):
        col.insert_one({"_subject": subject, "_user": str(uid)})
    col.update_one({"_subject": subject, "_user": str(uid)},  {"$set": {ltwo: hdiw}}, upsert=True)


def readresult(uid: str, subject: str) -> str:
    """client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client["userdata"]
    if f"{uid}:{subject}" in db:
        doc_rr = db[":".join((str(uid), subject))]
        document = doc_rr
        if "_id" in document:
            del document["_id"]
            del document["_rev"]
        client.disconnect()
        return document
    else:
        return "File not available"""""

    db = client[get_db_name()]
    col = db["userdata"]
    with suppress(Exception):
        return col.find_one({"_user": str(uid), "_subject": subject}, {"_id": 0, "_subject": 0, "_user": 0})


    # elif f"{uid}:{subject}" not in db:
    #    db.create_document({"_id": ":".join((uid, subject))})


def delete(uid: str, subject: str) -> str:
    try:
        os.remove(f"{getdatadir()}/userdata/{uid}/{subject}.json")
        return "Success"
    except:
        return "Error"
