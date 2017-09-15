from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
app = Flask(__name__)
app.secret_key = "KeepItSecretKeepItSafe"
mysql = MySQLConnector(app,'friendsdb')
@app.route('/users', methods=["GET"])
def index():
    query = "SELECT id, CONCAT(first_name, ' ', last_name) AS full_name, email, DATE_FORMAT(created_at, '%M %D, %Y') AS date FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)

@app.route('/users/new', methods=['GET'])
def new():
    return render_template("new.html")

@app.route("/users/<id>/edit", methods=["GET"])
def edit(id):
    query = "SELECT first_name, last_name, email FROM friends WHERE id = :id"
    data = {'id': id}
    friends = mysql.query_db(query, data)
    return render_template("edit.html", id=id, friend=friends[0])

@app.route("/users/<id>", methods=["GET"])
def show(id):
    query = "SELECT CONCAT(first_name, ' ', last_name) AS full_name, email, DATE_FORMAT(created_at, '%M %D, %Y') AS date FROM friends WHERE id = :id"
    data = {'id': id}
    friends = mysql.query_db(query, data)
    return render_template("show.html", id=id, friend=friends[0])

@app.route("/users/create", methods=["POST"])
def create():
    valid = True
    if len(request.form["first_name"]) < 1:
        flash("First name must not be blank!", "reg")
        valid = False
    elif len(request.form["first_name"]) < 2:
        flash("First name must be at least 2 letters!", "reg")
        valid = False
    elif not LETTER_REGEX.match(request.form["first_name"]):
        flash("First name must be letters only!", "reg")
        valid = False
    if len(request.form["last_name"]) < 1:
        flash("Last name cannot be blank!", "reg")
        valid = False
    elif len(request.form["last_name"]) < 2:
        flash("Last name must be at least 2 letters!", "reg")
        valid = False
    elif not LETTER_REGEX.match(request.form["last_name"]):
        flash("Last name must be letters only!", "reg")
        valid = False
    if len(request.form["email"]) < 1:
        flash("Email must not be blank!", "reg")
        valid = False
    elif not EMAIL_REGEX.match(request.form["email"]):
        flash("Invalid email!", "reg")
        valid = False
    if valid:
        query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
        data = {
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'email': request.form['email']
            }
        newid = mysql.query_db(query, data)
        return redirect('/users/'+str(newid))
    else:
        return redirect("/users/new")

@app.route('/users/<id>/destroy', methods=['GET'])
def delete(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/users')

@app.route('/users/<id>/update', methods=['POST'])
def update(id):
    valid = True
    if len(request.form["first_name"]) < 1:
        flash("First name must not be blank!", "reg")
        valid = False
    elif len(request.form["first_name"]) < 2:
        flash("First name must be at least 2 letters!", "reg")
        valid = False
    elif not LETTER_REGEX.match(request.form["first_name"]):
        flash("First name must be letters only!", "reg")
        valid = False
    if len(request.form["last_name"]) < 1:
        flash("Last name cannot be blank!", "reg")
        valid = False
    elif len(request.form["last_name"]) < 2:
        flash("Last name must be at least 2 letters!", "reg")
        valid = False
    elif not LETTER_REGEX.match(request.form["last_name"]):
        flash("Last name must be letters only!", "reg")
        valid = False
    if len(request.form["email"]) < 1:
        flash("Email must not be blank!", "reg")
        valid = False
    elif not EMAIL_REGEX.match(request.form["email"]):
        flash("Invalid email!", "reg")
        valid = False
    if valid:
        query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
        data = {
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'email': request.form['email'],
                'id': id
            }
        mysql.query_db(query, data)
        return redirect('/users/'+str(id))
    else:
        return redirect("/users/"+str(id)+"/edit")

app.run(debug=True)
