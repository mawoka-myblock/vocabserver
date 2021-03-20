import os
from fastapi import Form

global response
response = "hallo"
def save(subject, classroom, id, l1, l2):
    try:
        os.mkdir("./data/" + classroom)
        os.mkdir("./data/" + classroom + "/" + subject)
        f = open(os.path.join('./data/' + classroom + '/' + subject, id + ".txt"), "a")
        # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
        f.write(l1)
        f.write(" : ")
        f.write(l2)
        f.write("\n")
        f.close()
        response = "Success"
    except:
        try:
            f = open(os.path.join('./data/' + classroom + '/' + subject, id + ".txt"), "a")
            # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
            f.write(l1)
            f.write(" : ")
            f.write(l2)
            f.write("\n")
            f.close()
            response = "Success"
        except:
            response = "Error"


def read(subject, classroom, id):
    try:
        with open(os.path.join('./data/' + classroom + '/' + subject, id + '.txt'), "r" ) as f:
            content = f.readline()
        response = content
        return content
    except:
        return "Error 128596335"