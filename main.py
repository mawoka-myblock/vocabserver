from flask import Flask, render_template, url_for, request, redirect, g, render_template_string
from flask_sqlalchemy import SQLAlchemy
import auth
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


import flask

app = flask.Flask(__name__)

app.secret_key = 'hjfzguzhnuhrgh87jzuizfhij8junhrt86zth8jz7hdzgzfu7ur8hajtdsk8hggftae76sgufgud'  # Change this!
import datahandler
#app.add_url_rule('/api/add-list/<subject>/<classroom>/<id>', view_func=datahandler.savethings, methods=['GET', 'POST', 'DELETE'])

#app.add_url_rule('/api/read-list/<subject>/<classroom>/<id>', view_func=datahandler.readlists)




if __name__ == '__main__':
    app.run(debug=True)
