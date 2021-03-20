from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Form, Depends
import datahandler
import secrets

# import users

app = FastAPI()

response = datahandler.response





# @app.get("/users/me")
# def read_current_user(username: str = Depends(users.get_current_username)):
#    return {"username": username}


import databases
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

DATABASE_URL = "sqlite:///test.db"
SECRET = "SECRET"
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


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


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login")

fastapi_users = FastAPIUsers(user_db, [jwt_authentication], User, UserCreate, UserUpdate, UserDB, )
app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(SECRET, after_forgot_password=on_after_forgot_password),
                   prefix="/auth", tags=["auth"], )
app.include_router(fastapi_users.get_verify_router(SECRET, after_verification_request=after_verification_request),
                   prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

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


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/read-list/{subject}/{classroom}/{id}", tags=["vocabapi"], auth=True)
async def update_item(subject: str, classroom: str, id: str):
    return datahandler.read(subject, classroom, id)


@app.post("/api/add-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update_item(subject: str, classroom: str, id: str, lone: str = Form(default=None),
                      ltwo: str = Form(default=None)):
    return datahandler.save(subject, classroom, id, lone, ltwo)
