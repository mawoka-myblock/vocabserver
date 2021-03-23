import configparser

config = configparser.ConfigParser()

config['DIRECTORY'] = {'Data': './data'}


def getdatadir():
    config.read('config.ini')
    return config["DIRECTORY"]['Data']