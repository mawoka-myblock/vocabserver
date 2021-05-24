from config import sentry, geturl, mail
sentry()
import requests
from icecream import ic
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os


def verify(token):
    print("HALLO1")
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    ic()
    r = requests.post("http://127.0.0.1:8000/api/v1/auth/verify", data='{"token": "%s"}' % token, headers=headers)
    print(r.text)
    #r = requests.post("https://bin.muetsch.io/xgom6ya", data='{"token": "%s"}' % token, headers=headers)
    #return r.text
    #ic(r.text)

def requestverify(usermail):
    print(usermail)
    r = requests.post("http://127.0.0.1:8000/api/v1/auth/request-verify-token", data='{"email": "%s"}' % usermail.replace("%40", "@"))
    return r.text


def sendmail(email, token):
    import smtplib
    env = Environment(
        loader=FileSystemLoader('templates/'))
    #print(f"Verification requested for user {email}. Verification token: {token}")
    #sender = "<vocabserver@lol.org>"
    #receiver = f"<{user.email}>"
    template = env.get_template("registertemplate.html")
    html = template.render({"link": f"{geturl()}/static/verify.html?id={token}"})
    message = MIMEMultipart()
    message["Subject"] = "Verify your email"
    message["From"] = mail("adress")
    message["To"] = email
    message.attach(MIMEText(html, "html"))
    msgbody = message.as_string()

    with smtplib.SMTP(mail("serveradress"), mail("port")) as server:
        server.ehlo()
        server.starttls()
        server.login(mail("username"), mail("password"))
        server.sendmail(mail("adress"), email, msgbody)



def passwordresetmail(email, token):
    import smtplib
    env = Environment(
        loader=FileSystemLoader('templates/'))
    template = env.get_template("passwordreset.html")
    html = template.render({"link": f"{geturl()}/static/passwordreset.html?id={token}"})
    message = MIMEMultipart()
    message["Subject"] = "Verify your email"
    message["From"] = mail("adress")
    message["To"] = email
    message.attach(MIMEText(html, "html"))
    msgbody = message.as_string()

    with smtplib.SMTP(mail("serveradress"), mail("port")) as server:
        server.ehlo()
        server.starttls()
        server.login(mail("username"), mail("password"))
        server.sendmail(mail("adress"), email, msgbody)