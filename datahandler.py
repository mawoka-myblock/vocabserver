import os
from fastapi import Form

global response
response = "hallo"


def save(subject, classroom, id, l1, l2):
    try:
        os.mkdir("./data/vocab/" + classroom)
        os.mkdir("./data/vocab/" + classroom + "/" + subject)
        f = open(os.path.join('./data/' + classroom + '/' + subject, id + ".txt"), "a")
        # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
        f.write(l1)
        f.write(" : ")
        f.write(l2)
        f.write("\n")
        f.close()
        response = "Success"
        print(response)
    except:
        try:
            f = open(os.path.join('./data/vocab/' + classroom + '/' + subject, id + ".txt"), "a")
            # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
            f.write(l1)
            f.write(" : ")
            f.write(l2)
            f.write("\n")
            f.close()
            response = "Success"
            print(response)
        except:
            response = "Error"
            print(response)


print(response)


def read(subject, classroom, id):
    try:
        with open(os.path.join('./data/vocab/' + classroom + '/' + subject, id + '.txt'), "r") as f:
            content = f.readline()
        response = content
        return content
    except:
        return "Error 128596335"


def getcontent():
    firstdir = os.listdir(path="data/vocab")
    for i in firstdir:
        print(i)
