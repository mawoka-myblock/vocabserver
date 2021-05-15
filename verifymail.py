import sentry_sdk
sentry_sdk.init(
    "https://f09f3900a5304b768554e3e5cab68bcd@o661934.ingest.sentry.io/5764925",
    traces_sample_rate=1.0
)
import requests
from string import Template


def verify(token):
    print("HALLO1")
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = '{"token": "$"}'
    r = requests.post("http://127.0.0.1:8000/api/v1/auth/verify", data={"token": token}, headers=headers)
    return r.text

def requestverify(usermail):
    print("HALLO")
    r = requests.post("http://localhost:8000/auth/request-verify-token", data={"email": usermail})
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

    Please open this link: http://localhost:8000/api/v1/user/verifymail/{token}"""
    with smtplib.SMTP("smtp.ethereal.email", 587)as server:
        server.starttls()
        server.login("vida.jerde89@ethereal.email", "kZEpbJ3YWxgWyPd9Zk")
        server.sendmail(sender, receiver, message)