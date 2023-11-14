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

@app.route("/myrecipes/<int:user_id>")
def myrecipes(user_id):
    recipesinfo = [recipes.recipe_properties(x) for x in recipes.users_recipes(user_id)]
    return render_template("myrecipes.html", recipes = recipesinfo)

@app.route("/addrecipe", methods = ["post", "get"])
def addrecipe():
    if request.method == "GET":
        return render_template("addrecipe.html")
    if request.method == "POST":
        name = request.form["name"]
        time = request.form["time"]
        desc = request.form["description"]
        ingr = request.form["ingredients"]
        inst = request.form["instructions"]
        priv = True
        user = request.form["user_id"]

        recipes.add_recipe(user, name, desc, time, priv, ingr, inst)
    
        return redirect("/myrecipes/"+str(user))



