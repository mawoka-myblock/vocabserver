import os
from contextlib import suppress

global response
from config import getdatadir
import json
import codecs
from icecream import ic



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
    """
    with suppress(Exception):
        # print("H")
        os.mkdir(f"{getdatadir()}/vocab/" + classroom)
        os.mkdir(f"{getdatadir()}/vocab/" + classroom + "/" + subject)
        # print("I")
        f = open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "w")
        data = {l1: l2}
        json.dump(data, f)
        f.close()
        # print("Hallo")
        savetoindex(classroom, id, subject)
        return "Success"
    try:
        with suppress(Exception):
            # print("J")
            f = open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "r")
            # print("K")
            data = json.load(f)
            f.close()
        # print("ö")
        f = open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "w")
        data.update({l1: l2})
        json.dump(data, f)
        # print("Moin")
        savetoindex(classroom, id, subject)
        # print("Kein Fehler")
        return "Success"
    except:
        f = open(os.pThe TLS protocol is used to encrypt communications across a network to ensure that transmitted data remains private. There are three released versions of TLS: 1.0, 1.1, and 1.2. All HTTPS connections use TLS.

ath.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + '/' + id + ".json"), "w")
        # print("Hallo")
        data = {l1: l2}
        json.dump(data, f)
        f.close()
        # print("Hallo")
        savetoindex(classroom, id, subject)
        return "Success"
        """


def read(subject, classroom, id):
    try:
        with open(os.path.join(f'{getdatadir()}/vocab/' + classroom + '/' + subject + "/" + id + '.json'), "r") as f:
            return json.load(f)
    except:
        return ic()


def getcontent(subject, classroom):
    try:
        with open(os.path.join(f'./{getdatadir()}/vocab/{classroom}/{subject}/index.json'), "r") as f:
            index = json.load(f)
        return index
    except Exception:
        return ic()


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
