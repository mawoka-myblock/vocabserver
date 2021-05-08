import json
import os

global data
from config import getdatadir


def saveresult(uid, ltwo, hdiw, subject):
    content = os.listdir(f"{getdatadir()}/userdata/{uid}")
    try:
        with open(f'{getdatadir()}/userdata/{uid}/{subject}.json', "r") as f:
            data = json.load(f)
        data.update({ltwo: hdiw})
        with open(f'{getdatadir()}/userdata/{uid}/{subject}.json', "w") as f:
            json.dump(data, f)
        return "Success"
    except:
        try:
            with open(f'{getdatadir()}/userdata/{uid}/{subject}.json', "w") as f:
                data = {ltwo: hdiw}
                json.dump(data, f)
            return "Success"
        except:
            return "Error"


def readresult(uid, subject):
    try:
        with open(f"{getdatadir()}/userdata/{uid}/{subject}.json", "r") as f:
            return json.load(f)
    except:
        return "File not available"


def delete(uid, subject):
    try:
        os.remove(f"{getdatadir()}/userdata/{uid}/{subject}.json")
        return "Success"
    except:
        return "Error"
