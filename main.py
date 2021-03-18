from flask import Flask, render_template, url_for, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
import flask_login

import flask
app = flask.Flask(__name__)
app.secret_key = 'hjfzguzhnuhrgh87jzuizfhij8junhrt86zth8jz7hdzgzfu7ur8hajtdsk8hggftae76sgufgud'  # Change this!





@app.route('/api/add-post', methods = ['GET', 'POST', 'DELETE'])
def user():
    if request.method == 'GET':
        """return the information for <user_id>"""

    if request.method == 'POST':
        # changes
        data = request.form['content']
        f = open("testfile.txt", "a")
        f.write(data)
        f.close()

    else:
        # POST Error 405 Method Not Allowed
        return "Error"



if __name__ == '__main__':
    app.run(debug=True)
