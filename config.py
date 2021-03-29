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
