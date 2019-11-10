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

@app.route('/user', methods = ["GET"])
def userlogin():
    return render_template("userlogin.html")

@app.route('/user/mykeys', methods = ["POST"])
def userkeys():
    if "inputusername" in request.form:
        if not user_login(db, request.form["inputusername"]):
            return render_template("error.html", mainerror = "Sorry", suberror = "Unable to Log In")

        mis = request.form["inputusername"]

        accessible_keys_stored = get_accessible_placed_keys(db, mis)
        accessible_keys_held_by_others = get_accessible_held_keys(db, mis)
        keys_you_have = get_keys_held(db, mis)

        print(accessible_keys_stored)

        return render_template("keys.html", stored = accessible_keys_stored, others = accessible_keys_held_by_others, held = keys_you_have)


@app.route('/admin', methods = ["GET"])
def adminjobs():
    return render_template("admin.html")

@app.route('/admin/placekeys', methods = ["POST"])
def managekeys():
    pid = int(list(request.form.keys())[0])
    return str(list(map(lambda x: x[0], getkeys_of_place(db, pid))))

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


@app.route('/admin/clubs', methods = ["GET", "POST"])
def manageclubs():
    error = None
    if request.method == "POST":
        print("GOT A NEW PLACE", request.form)
        if "add" in request.form:
            print("I AM INSIDE CLUB")
            placename = request.form['newclub']
            manager = request.form['manager']
            retval = registerclub(db, placename, manager)
            if retval == ALREADYREGISTERED:
                error = "Duplicate Place"
            elif retval == INVALIDMANAGER:
                error = "Manager chosen invalid"
            elif retval != 0:
                error = "Unable to register club" + placename
        else:
            print("GOT A CHANGE REQUEST", request.form, request.args)

    club_data = getclubs(db)
    return render_template("clubs.html", clubs =  club_data, error = error)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000)
