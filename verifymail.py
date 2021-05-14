import requests


def verify(token):
    print("HALLO1")
    r = requests.post("http://localhost:8000/api/v1/auth/verify", data={"token": token})
    return r.text

def requestverify(usermail):
    print("HALLO")
    r = requests.post("http://localhost:8000/api/v1/auth/request-verify-token", data={"email": usermail})
    return r.text