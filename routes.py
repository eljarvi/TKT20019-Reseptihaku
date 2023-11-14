from app import app
from flask import render_template, request, redirect
import recipes
import users

@app.route("/")
def index():
    return render_template("index.html", recipes_count = len(recipes.all_recipes()))

@app.route("/login", methods = ['post', 'get'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if users.login(user, password):
            return redirect("/")
        else:
            return render_template("login.html")

@app.route("/register", methods = ['post', 'get'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

