import os

global response
from config import getdatadir
import json


# def savetoindex(path):
#        with open(os.path.join('data/vocab/index.json'), "rb") as f:
#            index = pickle.load(f)
#        if index != "":
#            with open(os.path.join('data/vocab/index.json'), "wb") as f:
#                index = [index, "data/vocab/" + path]
#                pickle.dump(index, f)
#        else:
#            with open(os.path.join('data/vocab/index.json'), "wb") as f:
#                index = ["data/vocab/" + path]
#                pickle.dump(index, f)
#        return "success"

def savetoindex(path):
    try:
        try:
            with open(os.path.join(f'{getdatadir()}/vocab/index.json'), "r") as f:
                index = json.load(f)
            index.append(path)
            with open(os.path.join(f'{getdatadir()}/vocab/index.json'), "w") as f:
                json.dump(index, f, indent=2)
            print("Success")
        except:
            index = [path]
            with open(os.path.join(f'{getdatadir()}/vocab/index.json'), "w") as f:
                json.dump(index, f, indent=2)
            print("Success")
    except:
        print("Error")


def save(subject, classroom, id, l1, l2):
    try:
        print("H")
        os.mkdir(f"{getdatadir()}/vocab/" + classroom)
        os.mkdir(f"{getdatadir()}/vocab/" + classroom + "/" + subject)
        print("I")
        f = open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "w")
        data = {l1: l2}
        json.dump(data, f)
        f.close()
        print("Hallo")
        fullpath = classroom + "/" + subject + "/" + id + ".json"
        savetoindex(fullpath)
        return "Success"
    except:
        print("J")
        f = open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "r")
        print("K")
        data = json.load(f)
        f.close()
        f = open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "w")
        data.update({l1: l2})
        json.dump(data, f)
        print("Moin")
        fullpath = classroom + "/" + subject + "/" + id + ".json"
        savetoindex(fullpath)
        return "Success"


def read(subject, classroom, id):
    try:
        with open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + "/" + id + '.json'), "r") as f:
            return json.load(f)
    except:
        return "Error 128596335"


def getcontent():
    with open(os.path.join(f'./{getdatadir()}/vocab/index.json'), "r") as f:
        index = json.load(f)
    return index


# TODO: NEU MACHEN!!!


def editcontent(subject, classroom, id, lone, ltwo):
    return "NEEDS TO BE DONE AFTER WRITING STH ELSE IN JSON!!!"
