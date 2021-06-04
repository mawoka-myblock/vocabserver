#import sentry_sdk
#sentry_sdk.init(environment="development")
#sentry_sdk.init(
#    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
#    traces_sample_rate=1.0
#)
import configparser
import os
import sys
config = configparser.ConfigParser()

#config['DIRECTORY'] = {'Data': './data'}


def getdatadir():
    config.read('config.ini', encoding='utf-8-sig')
    return config["DIRECTORY"]['Data']


def getport():
    config.read('config.ini', encoding='utf-8-sig')
    return config["SERVER"]['Port']


def debug():
    config.read('config.ini', encoding='utf-8-sig')
    if config["SERVER"]['Debug']:
        return "True"
    else:
        return False


def passwdlength():
    config.read('config.ini', encoding='utf-8-sig')
    return config["SECURITY"]["Mininmal_Password_Length"]


def getsecret():
    config.read('config.ini', encoding='utf-8-sig')
    if config["SECURITY"]["Secret"] == "CHANGE ME":
        sys.exit()
    else:
        return config["SECURITY"]["Secret"]


def geturl():
    config.read("config.ini", encoding='utf-8-sig')
    return config["FRONTEND"]["API_Url"]

def getdb(arg):
    os.getenv("CouchDB_USERNAME", "admin")

    config.read("config.ini", encoding='utf-8-sig')
    if arg == "uname":
        return os.getenv("CouchDB_USERNAME", "admin")
    elif arg == "passwd":
        return os.getenv("CouchDB_PASSWORD", "password")
    elif arg == "url":
        return os.getenv("CouchDB_URL", "http://127.0.0.1:5984")
    else:
        print("Wrong Arg")
        exit()

def get_sentry_url():
    config.read("config.ini", encoding='utf-8-sig')
    return config["SENTRY"]["Url"]
def get_sentry_trs():
    config.read("config.ini", encoding='utf-8-sig')
    return config["SENTRY"]["traces_sample_rate"]
def get_sentry_env():
    config.read("config.ini", encoding='utf-8-sig')
    return config["SENTRY"]["environment"]

def sentry():
    """config.read("config.ini")
    import sentry_sdk
    sentry_sdk.init(
        config["SENTRY"]["Url"],
        traces_sample_rate=float(config["SENTRY"]["traces_sample_rate"]), environment=config["SENTRY"]["environment"]
    )"""
    pass

def mail(thing):
    config.read("config.ini", encoding='utf-8-sig')
    if thing == "adress":
        return config["MAIL"]["Mailadress"]
    elif thing == "password":
        return config["MAIL"]["Password"]
    elif thing == "username":
        return config["MAIL"]["username"]
    elif thing == "serveradress":
        return config["MAIL"]["serveradress"]
    elif thing == "port":
        return int(config["MAIL"]["port"])
    else:
        print("You Idiot!")


