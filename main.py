from flask import Flask, render_template, url_for, request, redirect, g, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json



app = Flask(__name__)
auth = HTTPBasicAuth()

user = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}
with open('data/users.json', 'w') as file:
    json.dump(user, file)

with open('data/users.json', 'r') as f:
  users = json.loads(f)


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


import datahandler #Has the following urls: /api/add-list/<subject>/<classroom>/<id>  and   /api/read-list/<subject>/<classroom>/<id>

print(users)


if __name__ == '__main__':
    app.run(debug=True)
