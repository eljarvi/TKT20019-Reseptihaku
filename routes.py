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
    users.check_user(user_id)
    recipesinfo = [recipes.recipe_properties(x) for x in recipes.users_recipes(user_id)]
    return render_template("myrecipes.html", recipes = recipesinfo)

@app.route("/addrecipe", methods = ["post", "get"])
def addrecipe():
    if request.method == "GET":
        users.require_login()
        return render_template("addrecipe.html")
    if request.method == "POST":
        user = request.form["user_id"]
        users.check_user(int(user))
        name = request.form["name"]
        time = request.form["time"]
        if not time.isdigit():
            time = -1
        desc = request.form["description"]
        ingr = request.form["ingredients"]
        inst = request.form["instructions"]
        priv = request.form["privacy"]
    
        recipes.add_recipe(user, name, desc, time, priv, ingr, inst)
    
        return redirect("/myrecipes/"+str(user))

@app.route("/recipe/<int:recipe_id>", methods = ["get"])
def recipe(recipe_id):
    if request.method == "GET":
        recipeinfo = recipes.recipe_properties(recipe_id)
        if recipeinfo[5]:  # if the recipe is private
            users.check_user(recipeinfo[1])
        if recipeinfo[4] == -1: 
            time = "-"
        else:
            time = recipeinfo[4] 
        ingr = recipes.recipe_ingredients(recipe_id)
        inst= recipes.recipe_instructions(recipe_id)
        return render_template("recipe.html", id = recipe_id, owner_id = recipeinfo[1], name = recipeinfo[2], description = recipeinfo[3], time = time, ingredients =ingr, instruction = inst)

@app.route("/delete", methods = ["post"])
def delete():
    if request.method == "POST":
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        recipes.remove_recipe(recipe_id)
        return redirect("/myrecipes/"+user_id)

@app.route("/modify", methods = ["post"])
def modify():
    if request.method == "POST":
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        id = request.form["recipe_id"]
        recipeinfo = recipes.recipe_properties(id)
        ingr = recipes.recipe_ingredients(id)
        inst = recipes.recipe_instructions(id)
        return render_template("modify.html", id = id, name = recipeinfo[2], desc=recipeinfo[3], time = recipeinfo[4], priv = recipeinfo[5], ingredients = ingr, instructions = inst)

@app.route("/savechanges", methods = ["post"])
def savechanges():
    if request.method == "POST":
        recipe_id = request.form["recipe_id"]
        owner_id = recipes.recipe_properties(recipe_id)[1]
        users.check_user(owner_id)
        new_name = request.form["name"].strip()
        new_desc = request.form["description"].strip()
        new_time = request.form["time"]
        if not new_time.isdigit():
            new_time = -1
        new_priv = request.form["privacy"]
        recipes.change_recipe_properties(recipe_id, new_name, new_desc, new_time, new_priv)
        new_inst = request.form["instructions"]
        recipes.change_recipe_instructions(recipe_id, new_inst)
        new_ings = request.form["ingredients"].strip().split("\n")
        for ing in new_ings:
            parts = ing.split(";")
            if len(parts) == 2:
                recipes.add_ingredient(recipe_id, parts[0].strip(), parts[1].strip())

        removed = request.form.getlist("removed")
        for ing in removed:
            recipes.remove_ingredient(ing)
        
    return redirect("/recipe/"+recipe_id)

@app.route("/search", methods = ["post", "get"])
def search():
    if request.method == "GET":
        recipesinfo = [recipes.recipe_properties(x) for x in recipes.all_recipes()]
        return render_template("search.html", recipes = recipesinfo, name_search = "", maxtime = "", ing_search = "")
    if request.method == "POST":
        name= request.form["name"]
        time = request.form["time"]
        ingredients = request.form["ingredient"].strip()
        ingredientlist = [x.strip().lower() for x in ingredients.split(",")]
        recipesinfo = [recipes.recipe_properties(x) for x in recipes.search_recipes(name, time, ingredientlist)]
        return render_template("search.html", recipes = recipesinfo, name_search = name, maxtime = time, ing_search = ingredients)










