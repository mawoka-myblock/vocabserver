import sentry_sdk
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
from fastapi import FastAPI, Depends, Form, File, UploadFile
from fastapi.responses import JSONResponse

import auth
import datahandler
import students
from auth import User, SECRET, JWTAuthentication
from docs import tags_metadata
from fastapi.responses import ORJSONResponse
from pywebio.platform.fastapi import webio_routes
import interface.ui as ui
from fastapi.staticfiles import StaticFiles
import initialisation
import verifymail





app = FastAPI(title="Vocabserver", version="0.0.1", openapi_tags=tags_metadata)
initialisation.init(True)

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="/api/v1/auth/jwt/login")
jwt_stay_auth = JWTAuthentication(secret=SECRET, lifetime_seconds=1209600, tokenUrl="/api/v1/auth/jwt/stay-login")

fastapi_users = auth.FastAPIUsers(auth.user_db, [jwt_authentication], User, auth.UserCreate, auth.UserUpdate,
                                  auth.UserDB, )
app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/api/v1/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_auth_router(jwt_stay_auth), prefix="/api/v1/auth/jwt-stay", tags=["auth"])
app.include_router(fastapi_users.get_register_router(auth.on_after_register), prefix="/api/v1/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(SECRET, after_forgot_password=auth.on_after_forgot_password),
    prefix="/api/v1/auth", tags=["auth"], )
app.include_router(
    fastapi_users.get_verify_router(SECRET, after_verification_request=auth.after_verification_request),
    prefix="/api/v1/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(), prefix="/api/v1/users", tags=["users"])
verified_user = fastapi_users.current_user(verified=True)


@app.get("/api/v1/vocab/read-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update_item(subject: str, classroom: str, id: str, user: User = Depends(verified_user)):
    return datahandler.read(subject, classroom, id)


@app.post("/api/v1/vocab/add-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update_item(subject: str, classroom: str, id: str, lone: str = Form(default=None),
                      ltwo: str = Form(default=None), user: User = Depends(verified_user)):
    return datahandler.save(subject, classroom, id, lone, ltwo)


@app.get("/api/v1/vocab/list-list/{subject}/{classroom}", tags=["vocabapi"])
async def index(classroom: str, subject: str, user: User = Depends(verified_user)):
    return JSONResponse(content=datahandler.getcontent(subject, classroom))
# Will return overview about available chapters


@app.post("/api/v1/students/write-stats/{subject}", tags=["students"])
async def index(subject: str, ltwo: str = Form(default=None), hdiw: str = Form(default=None),
                user: User = Depends(verified_user)):  # hdiw = how did it work
    return students.saveresult(user.id, ltwo, hdiw, subject)


@app.get("/api/v1/students/get-stats/{subject}", tags=["students"])
async def index(subject: str, user: User = Depends(verified_user)):
    return students.readresult(user.id, subject)


@app.delete("/api/v1/students/delete-stats/{subject}", tags=["students"])
async def delete(subject: str, user: User = Depends(verified_user)):
    return students.delete(user.id, subject)


@app.patch("/api/v1/vocab/edit-list/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def update(subject: str, classroom: str, id: str, lone: str = Form(default=None), ltwo: str = Form(default=None),
                 user: User = Depends(verified_user)):
    return datahandler.editcontent(subject, classroom, id, lone, ltwo)


@app.post("/api/v1/vocab/upload/{subject}/{classroom}/{id}", tags=["vocabapi"])
async def index(subject: str, classroom: str, id: str, file: UploadFile = File(default=None), user: User = Depends(verified_user)):
    filecontent = await file.read()
    datahandler.filehandler(subject, classroom, id, filecontent)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/tool", FastAPI(routes=webio_routes(ui.login), cdn=False))
@app.get("/api/v1/user/verifymail/{verify_id}", tags=["users"])
async def index(verify_id: str):
    return verifymail.verify(verify_id)

@app.get("/api/v1/user/startverify/{usermail}", tags=["users"])
async def index(usermail: str):
    return verifymail.requestverify(usermail)


app.mount("/codemirror", StaticFiles(directory="static/codemirror"), name="codemirror")
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/image", StaticFiles(directory="static/image"), name="image")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/", FastAPI(routes=webio_routes(ui.login, cdn=False)))
