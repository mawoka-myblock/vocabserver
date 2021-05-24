from config import sentry, geturl
sentry()
import requests
from icecream import ic
from string import Template


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
    #print(f"Verification requested for user {email}. Verification token: {token}")
    #sender = "<vocabserver@lol.org>"
    #receiver = f"<{user.email}>"
    sender = "<jo.wyman@ethereal.email>"
    receiver = f"<{email}>"
    print(receiver, sender)
    message = f"""\
    Subject: verify your mail!
    To: {receiver}
    From: {sender}

    Please open this link: {geturl()}/static/verify.html/?id={token}"""
    with smtplib.SMTP("smtp.ethereal.email", 587) as server:
        server.starttls()
        server.login("vida.jerde89@ethereal.email", "kZEpbJ3YWxgWyPd9Zk")
        server.sendmail(sender, receiver, message)