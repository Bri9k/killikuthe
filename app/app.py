#!flask/usr/bin/python3
from flask import Flask, render_template, request
from modifications import *
from queries import *
from database import database
from config import KILLIDBCONFIG

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = database(KILLIDBCONFIG)

@app.route('/', methods = ['GET'])
def main_screen():
    return render_template("index.html")

@app.route('/register', methods = ['GET'])
def registration():
    return render_template("register.html")

@app.route('/keys', methods= ['POST'])
def signin_register():
    print("Request", request)
    print("Form Is Empty", request.form)
    firstname = request.form.get('firstName')
    lastname = request.form['lastName']
    mis = request.form['username']
    email = request.form['email'] 
    phoneno = request.form['phoneno']

    registered = registeruser(db, mis, firstname, lastname, phoneno, email)

    errorlist = [(LARGENAME, "Name too large"), (MISERROR, "MIS Invalid"), (EMAIL, "Email Invalid"), (WRONGNO, "Phone number invalid"), (ALREADYREGISTERED, "Invalid Registration")]
    if registered != 0:
        for error in errorlist:
            if registered == error[0]:
                print(error[1])
                message = error[1]
                break
            
        if not message:
            message = "Please try again"

        return render_template("register.html", error = message)

    return render_template("index.html")

@app.route('/admin', methods = ["GET"])
def adminjobs():
    return render_template("admin.html")

@app.route('/admin/places', methods = ["GET", "POST"])
def manageplaces():
    error = None
    if request.method == "POST":
        print("GOT A NEW PLACE", request.form)
        if "add" in request.form:
            print("I AM INSIDE")
            placename = request.form['newplace']
            if "isstorage" in request.form:
                store = True
            else:
                store = False
            retval = registerplace(db, placename, store)
            if retval == ALREADYREGISTERED:
                error = "Duplicate Place"
            elif retval != 0:
                error = "Unable to register place " + placename
        else:
            print("GOT A CHANGE REQUEST", request.form, request.args)

    place_data = getplaces(db)
    return render_template("places.html", places = place_data, error = error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000)
