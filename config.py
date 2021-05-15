import sentry_sdk
sentry_sdk.init(environment="development")
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
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
        return os.getenv("CouchDB_URL", "http://172.24.0.2:5984")
    else:
        print("Wrong Arg")
        exit()
