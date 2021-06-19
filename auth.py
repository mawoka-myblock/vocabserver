from config import sentry

sentry()

import databases
import sqlalchemy
from fastapi import FastAPI, Request
import fastapi_users
from pydantic import validator

from fastapi_users import models
from fastapi_users.db import MongoDBUserDatabase
import motor.motor_asyncio
from fastapi_users.authentication import JWTAuthentication

from config import getsecret, passwdlength, get_db_connection_str, get_db_name
import verifymail

FastAPIUsers = fastapi_users.FastAPIUsers

app = FastAPI()

#SECRET = getsecret()
SECRET = "85096eaaec2eccae28688159a87f26f490858bd7425e8b1cc40be4c2b99a9d1c8abc723640dadce389ec32ac9c2f1a74"


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < int(passwdlength()):
            raise ValueError(f'Password should be at least {int(passwdlength())} characters')
        return v


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


DATABASE_URL = get_db_connection_str()
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client[get_db_name()]
collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, collection)




def verification(uid, token):
    user = UserDB
    verifymail.sendmail(user.email, token)


def after_verification_request(user: UserDB, token: str, request: Request):
    verifymail.sendmail(user.email, token)


def on_after_register(user: UserDB, request: Request):
    # os.mkdir(f'{getdatadir()}/userdata/{user.id}')
    pass


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    verifymail.passwordresetmail(user.email, token)





@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
