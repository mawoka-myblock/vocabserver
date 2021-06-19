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


def getdatadir() -> str:
    config.read('config.ini', encoding='utf-8-sig')
    return config["DIRECTORY"]['Data']


def getport() -> int:
    config.read('config.ini', encoding='utf-8-sig')
    return int(config["SERVER"]['Port'])


def debug() -> bool:
    config.read('config.ini', encoding='utf-8-sig')
    if config["SERVER"]['Debug']:
        return True
    else:
        return False


def passwdlength() -> str:
    config.read('config.ini', encoding='utf-8-sig')
    return os.getenv("Mininmal_Password_Length", "8")


def getsecret() -> str:
    config.read('config.ini', encoding='utf-8-sig')
    """if config["SECURITY"]["Secret"] == "CHANGE ME":
        sys.exit()
    else:
        return config["SECURITY"]["Secret"]"""
    return os.getenv("Secret")


def geturl() -> str:
    config.read("config.ini", encoding='utf-8-sig')
    if os.getenv("Production", "false") == "false":
        return f"http://{os.getenv('MAIN_URL', 'localhost:8000')}"
    else:
        return f"https://{os.getenv('RAILWAY_STATIC_URL', '')}"
    #return "http://127.0.0.1:8000"

def getdb(arg: str) -> str:
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

def get_db_connection_str() -> str:
    #return os.getenv("Connection_string")
    return os.getenv("MONGO_URL", "")
    #return "mongodb+srv://LocalUser:e0qHZbe6VU1OsFJf@cluster0.yi3xs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


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

def mail(thing: str):
    config.read("config.ini", encoding='utf-8-sig')
    if thing == "adress":
        return os.getenv("MAILADRESS", "")
    elif thing == "password":
        return os.getenv("MAIL_PASSWORD")
    elif thing == "username":
        return os.getenv("MAILADRESS", "")
    elif thing == "serveradress":
        return os.getenv("MAIL_SERVER_ADRESS", "")
    elif thing == "port":
        return int(os.getenv("MAIL_SERVER_PORT", ""))
    else:
        print("You Idiot!")

def get_db_name() -> str:
    return os.getenv("DB_NAME", "vocabserver")


