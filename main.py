from fastapi import FastAPI, Form, Depends
from fastapi.responses import JSONResponse

import auth
import datahandler
import students
from auth import User, SECRET, JWTAuthentication
from docs import tags_metadata
#from pywebio.platform.fastapi import webio_routes
#import ui
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Vocabserver", version="0.0.1", openapi_tags=tags_metadata)

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login")

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
    return datahandler.save(subject, classroom, id, lone, ltwo)


@app.get("/api/vocab/list-list", tags=["vocabapi"])
async def index(user: User = Depends(verified_user)):
    return JSONResponse(content=datahandler.getcontent())


@app.post("/api/students/write-stats/{subject}", tags=["students"])
async def index(subject: str, ltwo: str, hdiw: str, user: User = Depends(verified_user)):  # hdiw = how did it work
    return students.saveresult(user.id, ltwo, hdiw, subject)


@app.get("/api/students/get-stats/{subject}", tags=["students"])
async def index(subject: str, user: User = Depends(verified_user)):
    return students.readresult(user.id, subject)


@app.delete("/api/students/delete-stats/{subject}", tags=["students"])
async def delete(subject: str, user: User = Depends(verified_user)):
    return students.delete(user.id, subject)


@app.patch("/api/vocab/edit-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update(subject: str, classroom: str, id: str, lone: str, ltwo: str, user: User = Depends(verified_user)):
    return datahandler.editcontent(subject, classroom, id, lone, ltwo)

#app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/tool", FastAPI(routes=webio_routes(ui.login), cdn=False))
