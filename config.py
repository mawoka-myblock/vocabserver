import configparser
import os
config = configparser.ConfigParser()

config['DIRECTORY'] = {'Data': './data'}


def getdatadir():
    config.read('config.ini')
    return config["DIRECTORY"]['Data']


def getport():
    config.read('config.ini')
    return config["SERVER"]['Port']


def debug():
    config.read('config.ini')
    if config["SERVER"]['Debug'] == True:
        return "True"
    else:
        return False


def passwdlength():
    config.read('config.ini')
    return config["SECURITY"]["Mininmal_Password_Length"]


def getsecret():
    config.read('config.ini')
    return config["SECURITY"]["Secret"]


def geturl():
    config.read("config.ini")
    return config["FRONTEND"]["API_Url"]

def getdb(arg):
    os.getenv("CouchDB_USERNAME", "admin")

    config.read("config.ini")
    if arg == "uname":
        return os.getenv("CouchDB_USERNAME", "admin")
    elif arg == "passwd":
        return os.getenv("CouchDB_PASSWORD", "password")
    elif arg == "url":
        return os.getenv("CouchDB_URL", "http://0.0.0.0:5984")
    else:
        print("Wrong Arg")
        exit()
