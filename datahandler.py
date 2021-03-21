import os
from fastapi import Form
import pickle
import json
import re
from collections import OrderedDict
global response
response = "hallo"


#def savetoindex(path):
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
    with open(os.path.join('data/vocab/index.json'), "a") as f:
        f.writelines(path + "\n")

    with open(os.path.join('data/vocab/index.json'), "r") as f:
        lines = f.readlines()
        lines_set = set(lines)
    with open(os.path.join('data/vocab/index.json'), "w") as f:
        for line in lines_set:
            f.write(line)


def save(subject, classroom, id, l1, l2):
    try:
        os.mkdir("./data/vocab/" + classroom)
        os.mkdir("./data/vocab/" + classroom + "/" + subject)
        f = open(os.path.join('./data/vocab/' + classroom + '/' + subject + '/ '+ id + ".txt"), "a")
        # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
        f.write(l1)
        f.write(" : ")
        f.write(l2)
        f.write("\n")
        f.close()
        fullpath = classroom + "/" + subject + "/" + id + ".txt"
        savetoindex(fullpath)
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
            fullpath = classroom + "/" + subject + "/" + id + ".txt"
            savetoindex(fullpath)
            response = "Success"
            print(response)
        except:
            response = "Error"
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
    with open(os.path.join('data/vocab/index.json'), "r") as f:
        index = f.read()
    index = index.strip()
    index = index.replace("\n", ";")
    return index
