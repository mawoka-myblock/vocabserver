from fastapi import FastAPI, Form, Depends

import auth
import datahandler
import students
from auth import User, SECRET
from docs import tags_metadata

app = FastAPI(title="Vocabserver", version="0.0.1", openapi_tags=tags_metadata)

response = datahandler.response

jwt_authentication = auth.JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login")

fastapi_users = auth.FastAPIUsers(auth.user_db, [jwt_authentication], User, auth.UserCreate, auth.UserUpdate,
                                  auth.UserDB, )
app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(auth.on_after_register), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(SECRET, after_forgot_password=auth.on_after_forgot_password),
    prefix="/auth", tags=["auth"], )
app.include_router(
    fastapi_users.get_verify_router(SECRET, after_verification_request=auth.after_verification_request),
    prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
verified_user = fastapi_users.current_user(verified=True)




@app.get("/api/vocab/read-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update_item(subject: str, classroom: str, id: str, user: User = Depends(verified_user)):
    return datahandler.read(subject, classroom, id)


@app.post("/api/vocab/add-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update_item(subject: str, classroom: str, id: str, lone: str = Form(default=None),
                      ltwo: str = Form(default=None), user: User = Depends(verified_user)):
    datahandler.save(subject, classroom, id, lone, ltwo)
    return datahandler.response


@app.get("/api/vocab/list-list", tags=["vocabapi"])
async def index(user: User = Depends(verified_user)):
    return datahandler.getcontent()


@app.post("/api/students/write-stats/{subject}", tags=["students"])
async def index(subject: str, user: User = Depends(verified_user),
                ltwo: str = Form(default=None),
                hdiw: str = Form(default=None)):  # hdiw = how did it work
    return students.saveresult(user.id, ltwo, hdiw, subject)

@app.get("/api/students/get-stats/{subject}", tags=["students"])
async def index(subject: str, user: User = Depends(verified_user)):
    return students.readresult(user.id, subject)
@app.delete("/api/students/delete-stats/{subject}", tags=["students"])
async def delete(subject: str, user: User = Depends(verified_user)):
    return students.delete(user.id, subject)

