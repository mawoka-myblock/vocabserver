import configparser

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

