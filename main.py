from flask import Flask, render_template, url_for, request, redirect, g, render_template_string
from flask_sqlalchemy import SQLAlchemy

import flask_login
#import os
#import stuff
import flask_login

import flask
app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
app.secret_key = 'hjfzguzhnuhrgh87jzuizfhij8junhrt86zth8jz7hdzgzfu7ur8hajtdsk8hggftae76sgufgud'  # Change this!
login_manager.init_app(app)


import datahandler
import auth

if __name__ == '__main__':
    app.run(debug=True)
