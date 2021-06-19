from config import sentry

sentry()
# from cryptography.fernet import Fernet

global response
from config import getdatadir, getdb, get_db_name, get_db_connection_str
import codecs
from pymongo import MongoClient
from icecream import ic
import os

client = MongoClient(get_db_connection_str())


def save(subject: str, classlevel: int, unit: str, l1: str, l2: str):
    """client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
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
    client.disconnect()"""
    db = client[get_db_name()]
    col = db[f"data_{classlevel}"]
    if type(col.find_one({"_subject": subject, "_unit": str(unit)})) == type(None):
        col.insert_one({"_subject": subject, "_unit": str(unit)})

    col.update_one({"_subject": subject, "_unit": str(unit)},
                   {"$set": {l2: l1}})
    return "Done"
    # TODO: Add document automatically


def read(subject, classlevel, id):
    """client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    doc = db[":".join((subject, id))]
    del doc["_id"]
    del doc["_rev"]
    return doc
    del doc
    client.disconnect()"""
    db = client[get_db_name()]
    col = db[f"data_{classlevel}"]
    return col.find_one({"_subject": subject, "_unit": id}, {"_id": 0, "_subject": 0, "_unit": 0})


def getcontent(subject, classlevel):  # The function to list the available "lists"
    """client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    liste = []
    #re.findall()
    for i in db:
        liste.append(i["_id"])
    result = []
    for i in liste:
        result.append(i.replace(f"{subject}:", ""))
    return result
    #return str(liste).replace(f"{subject}:", "")"""
    db = client[get_db_name()]
    col = db[f"data_{classlevel}"]
    return_obj = []
    for i in col.find({"_subject": "english"}, {"_unit": 1, "_id": 0}):
        return_obj.append(i["_unit"])
    return return_obj


# Will return overview about available chapters


def editcontent(subject, classlevel, id, lone, ltwo):
    """client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client[classlevel]
    doc = db[":".join((subject, id))]
    doc[lone] = ltwo
    doc.save()
    client.disconnect()
    return "Success"""""
    db = client[get_db_name()]
    col = db[f"data_{classlevel}"]
    col.update_one({"_subject": f"{subject} hallo", "_unit": id}, {"$set": {ltwo: lone}})
    return "Success"


def filehandler(subject, classroom, id, file):
    try:
        with open(os.path.join(f'{getdatadir()}/vocab/{classroom}/{subject}/{id}.json'), "w") as f:
            file_decoded = codecs.decode(file, "UTF-8")
            ic(file_decoded)
            f.write(file_decoded)
            # savetoindex(classroom, id, subject)
            return "Success"
    except Exception:
        return ic()


def stayloggedin(password, email, id):
    """client = CouchDB(getdb("uname"), getdb("passwd"), url=getdb("url"), connect=True)
    db = client["userdata"]
    doc_save = db[f"stayin:{id}"]
    document = doc_save
    document["loginid"] = loginid
    document.save()
    del document, doc_save"""
    db = client[get_db_name()]
    col = db["sli"]  # Stay Logged In
    col.insert_one({"user_id": id, "password": password, "email": email})
    return "Success"


def get_sli_data(loginid: str) -> str:
    db = client[get_db_name()]
    col = db["sli"]  # Stay Logged In
    return col.find_one({"user_id": loginid}, {"_id": 0})


def delete_sli(loginid: str):
    db = client[get_db_name()]
    col = db["sli"]  # Stay Logged In
    col.delete_one({"user_id": loginid})
    return "Ok"
