from flask import Flask, render_template, url_for, request, redirect, g
import flask_login
#import os
#import stuff


import flask
app = flask.Flask(__name__)
app.secret_key = 'hjfzguzhnuhrgh87jzuizfhij8junhrt86zth8jz7hdzgzfu7ur8hajtdsk8hggftae76sgufgud'  # Change this!

import datahandler

if __name__ == '__main__':
    app.run(debug=True)
