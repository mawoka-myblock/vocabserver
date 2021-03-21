import json
import os


def saveresult(uid, lone, ltwo, hdiw, subject, id):
    content = os.listdir(f"data/userdata/{uid}")
    for Number in range(len(content)):
        if list[Number] == subject:
            with open(f'data/userdata/{uid}/{lone}.json', "r") as f:
                data = json.load(f)
            with open(f'data/userdata/{uid}/{lone}.json', "w") as f:
                data.update({lone: hdiw})
                json.dump(data, f)
        else:
            dict: {ltwo: hdiw}
            with open(f'data/userdata/{uid}/{lone}.json', "w") as f:
                json.dump(dict, f)




