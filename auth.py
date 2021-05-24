from config import sentry

sentry()

import databases
import sqlalchemy
from fastapi import FastAPI, Request
import fastapi_users
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase
from pydantic import validator
from fastapi_users import models

from config import getdatadir, getsecret, passwdlength
import verifymail

FastAPIUsers = fastapi_users.FastAPIUsers

app = FastAPI()
DATABASE_URL = f"sqlite:///{getdatadir()}/users.db"
SECRET = getsecret()
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


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


class UserModel(OrmarBaseUserModel):
    class Meta:
        tablename = "users"
        metadata = metadata
        database = database


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

user_db = OrmarUserDatabase(UserDB, UserModel)


def verification(uid, token):
    user = UserDB
    verifymail.sendmail(user.email, token)


def after_verification_request(user: UserDB, token: str, request: Request):
    # sender = "<vocabserver@lol.org>"
    # receiver = f"<{user.email}>"
    verifymail.sendmail(user.email, token)


def on_after_register(user: UserDB, request: Request):
    # os.mkdir(f'{getdatadir()}/userdata/{user.id}')
    pass


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    verifymail.passwordresetmail(user.email, token)


app.state.database = database


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
