import uvicorn
import configparser


config = configparser.ConfigParser()
config.read("config.ini")
print(uvicorn.run("main:app", host=config["SERVER"]["Host"], port=config["SERVER"]["Port"], log_level=config["SERVER"]["Log_Level"]))