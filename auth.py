import databases
import json
import os
import requests
import smtplib
import sqlalchemy

from fastapi_users.authentication import JWTAuthentication
from fastapi import FastAPI, Request
from fastapi_users import models, FastAPIUsers
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase
from pydantic import validator

app = FastAPI()
DATABASE_URL = "sqlite:///users.db"
SECRET = "jkhgbvhfmgdjfjzgnhzvfzdcgjbnhzgrtg7hjjkt8hzoiig4uikzuhj78mio8z"
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < 6:
            raise ValueError('Password should be at least 6 characters')
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


def sendveriemail(uid, uname, token):
    sender = "Vocab Server <noreply@vocabserver.com"
    payload = {f"email: {uid}"}

    # token = r[]
    url = f"http://127.0.0.1:8000/user/verify{token}/{uid}"
    message = f"""\
    Subject: Verify yourself, pls!
    To: {uname}
    From: {sender}
    
    
    """

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("1cba579e59e62c", "70392fdcaa0ce4")
        server.sendmail(sender, uname, message)


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")
    sendveriemail(user.id, user.email, token)


def on_after_register(user: UserDB, request: Request):
    os.mkdir(f'data/userdata/{user.id}')
    print(f"User {user.id} has registered.")
    payload = {f"email: {user.id}"}
    r = requests.post("http://127.0.0.1:8000/auth/request-verify-token", data=json.dumps(payload))
    r = json.loads(r)

    sendveriemail(user.id, user.email, r)


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


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
