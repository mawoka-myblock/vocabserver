from flask import Flask, render_template, url_for, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
import flask_login
import os

import flask
app = flask.Flask(__name__)
app.secret_key = 'hjfzguzhnuhrgh87jzuizfhij8junhrt86zth8jz7hdzgzfu7ur8hajtdsk8hggftae76sgufgud'  # Change this!


@app.route('/api/add-list/<subject>/<classroom>/<id>', methods = ['GET', 'POST', 'DELETE'])
def save(subject, classroom, id):
    if request.method == 'GET':
        """return the information for <user_id>"""

    if request.method == 'POST':
        l1 = request.form['lone']
        l2 = request.form['ltwo']
        try:
            f = open(os.path.join('./data', id + ".txt"), "a")
            f.write(l1)
            f.write(" : ")
            f.write(l2)
            f.write("\n")
            f.close()
            return redirect("/")
        except:
            return "error 39615"
    else:
        # POST Error 405 Method Not Allowed
        return "Error"

if __name__ == '__main__':
    app.run(debug=True)
