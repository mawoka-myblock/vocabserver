import json
import os
global data


def saveresult(uid, ltwo, hdiw, subject):
    content = os.listdir(f"data/userdata/{uid}")
    print(content)
    if content != []:
        for Number in range(len(content)):
            print("hi")
            try:
                print("Hallo")
                with open(f'data/userdata/{uid}/{subject}.json', "r") as f:
                    data = json.load(f)
                data.update({ltwo: hdiw})
                with open(f'data/userdata/{uid}/{subject}.json', "w") as f:
                    json.dump(data, f)
                return "Success"
            except:
                try:
                    with open(f'data/userdata/{uid}/{subject}.json', "w") as f:
                        data = {ltwo: hdiw}
                        json.dump(data, f)
                    return "Success"
                except:
                    return "Error"

    #else:
    #    with open(f'data/userdata/{uid}/{subject}.json', "w") as f:
    #        data = {ltwo: hdiw}
     #       json.dump(data, f)



