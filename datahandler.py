from __main__ import app
import os
from flask import request
from auth import auth

@app.route('/api/add-list/<subject>/<classroom>/<id>', methods = ['GET', 'POST', 'DELETE'])
@auth.required
def savethings(subject, classroom, id):
    if request.method == 'GET':
        """return the information for <user_id>"""

    if request.method == 'POST':
        try:
            os.mkdir("./data/" + classroom)
            os.mkdir("./data/" + classroom + "/" + subject)
            f = open(os.path.join('./data/' + classroom + '/' + subject, id + ".txt"), "a")
            # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
            l1 = request.form['lone']
            l2 = request.form['ltwo']
            f.write(l1)
            f.write(" : ")
            f.write(l2)
            f.write("\n")
            f.close()
            return "Success"
        except:
            try:
                f = open(os.path.join('./data/' + classroom + '/' + subject, id + ".txt"), "a")
                # f = open(os.path.join('./data' + classroom, id + ".txt"), "a")
                l1 = request.form['lone']
                l2 = request.form['ltwo']
                f.write(l1)
                f.write(" : ")
                f.write(l2)
                f.write("\n")
                f.close()
                return "success"
            except:
                return "Error"


@app.route('/api/read-list/<subject>/<classroom>/<id>')
@auth.required
def readlists(subject, classroom, id):
    try:
        with open(os.path.join('./data/' + classroom + '/' + subject, id + '.txt'), "r" ) as f:
            content = f.readline()
        return content
    except:
        return "Error 128596335"
