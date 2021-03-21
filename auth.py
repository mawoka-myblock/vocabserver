import databases
import os
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


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


def on_after_register(user: UserDB, request: Request):
    os.mkdir(f'data/userdata/{user.id}')
    print(f"User {user.id} has registered.")


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
