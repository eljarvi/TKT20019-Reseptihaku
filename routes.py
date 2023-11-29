from flask import render_template, request, redirect
from app import app
import recipes
import users
import reviews

@app.route("/")
def index():
    return render_template("index.html", recipes_count = len(recipes.all_recipes()))

@app.route("/login", methods=['post', 'get'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if users.login(user, password):
            return redirect("/")
        return render_template("login.html")

@app.route("/register", methods=['post', 'get'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) >20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")
        password = request.form["password"]
        if len(password) < 5 or len(password)>50:
            return render_template("error.html", message="Salasanassa tulee olla 5-50 merkkiä")
        if users.register(username, password):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut")
""
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/myrecipes/<int:user_id>")
def myrecipes(user_id):
    users.check_user(user_id)
    recipesinfo = [recipes.recipe_properties(x) for x in recipes.users_recipes(user_id)]
    return render_template("myrecipes.html", recipes = recipesinfo)

@app.route("/addrecipe", methods=["post", "get"])
def addrecipe():
    if request.method == "GET":
        users.require_login()
        return render_template("addrecipe.html")
    if request.method == "POST":
        user = request.form["user_id"]
        users.check_user(int(user))
        name = request.form["name"]
        if len(name) <1 or len(name) > 50:
            return render_template("error.html", message = "Nimen tulee olla 1-50 merkkiä.")
        time = request.form["time"]
        if not time.isdigit() or time == 0:
            time = -1
        desc = request.form["description"]
        ingr_text = request.form["ingredients"].strip()
        ingr = [[x.strip() for x in pair.split(";")] for pair in ingr_text.split("\n")]
        for parts in ingr:
            if len(parts) != 2 or parts[0].strip() == "":
                return render_template(
                        "error.html",
                         message = "Raaka-aineet on syötettävä omille " +
                                "riveilleen muodossa raaka-aine;määrä.\n" +
                                "Jos et halua lisätä määrää kirjoita muodossa raaka-aine; . " +
                                "Raaka-ainekenttä ei voi olla tyhjä."
                        )
        inst = request.form["instructions"]
        priv = request.form["privacy"]
        recipes.add_recipe(user, name, desc, time, priv, ingr, inst)
        return redirect("/myrecipes/"+str(user))

@app.route("/recipe/<int:recipe_id>", methods=["get"])
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
        parameters = {
            "recipe_id" : recipe_id,
            "owner_id" : recipeinfo[1],
            "name" : recipeinfo[2],
            "description" : recipeinfo[3],
            "time": time,
            "ingredients" : ingr,
            "instruction" : inst,
            "reviewed": reviews.have_reviewed(users.get_user(), recipe_id),
            "reviews": reviews.recipe_reviews(recipe_id)
        }
        return render_template("recipe.html", **parameters)

@app.route("/delete", methods=["post"])
def delete():
    if request.method == "POST":
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        recipes.remove_recipe(recipe_id)
        return redirect("/myrecipes/"+user_id)

@app.route("/modify", methods=["post"])
def modify():
    if request.method == "POST":
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        recipeinfo = recipes.recipe_properties(recipe_id)
        ingr = recipes.recipe_ingredients(recipe_id)
        inst = recipes.recipe_instructions(recipe_id)
        parameters = {
            "id": recipe_id,
            "name": recipeinfo[2],
            "desc": recipeinfo[3],
            "time": recipeinfo[4],
            "priv": recipeinfo[5],
            "ingredients": ingr,
            "instructions": inst
        }
        return render_template("modify.html", **parameters)

@app.route("/savechanges", methods=["post"])
def savechanges():
    if request.method == "POST":
        recipe_id = request.form["recipe_id"]
        owner_id = recipes.recipe_properties(recipe_id)[1]
        users.check_user(owner_id)
        new_name = request.form["name"].strip()
        if len(new_name) < 1 or len(new_name) > 50:
            return render_template("error.html", message = "Nimen tulee olla 1-50 merkkiä.")
        new_desc = request.form["description"].strip()
        new_time = request.form["time"]
        if not new_time.isdigit():
            new_time = -1
        new_priv = request.form["privacy"]
        new_inst = request.form["instructions"]
        new_ings = request.form["ingredients"].strip()
        if not new_ings == "":
            for ing in new_ings.split("\n"):
                parts = ing.split(";")
                if len(parts) == 2:
                    if parts[0].strip() != "":
                        recipes.add_ingredient(recipe_id, parts[0].strip(), parts[1].strip())
                else:
                    return render_template(
                        "error.html",
                        message = "Raaka-aineet on syötettävä omille" +
                                    "riveilleen muodossa raaka-aine;määrä.\n" +
                                    "Jos et halua lisätä määrää kirjoita muodossa raaka-aine; ."
                            )

        removed = request.form.getlist("removed")
        for ing in removed:
            recipes.remove_ingredient(ing)

        recipes.change_recipe_properties(recipe_id, new_name, new_desc, new_time, new_priv)
        recipes.change_recipe_instructions(recipe_id, new_inst)

    return redirect("/recipe/"+recipe_id)

@app.route("/search", methods=["post", "get"])
def search():
    if request.method == "GET":
        recipesinfo = [recipes.recipe_properties(x) for x in recipes.all_recipes()]
        return render_template("search.html", recipes=recipesinfo,
                                name_search="", maxtime="", ing_search=""
                )
    if request.method == "POST":
        name= request.form["name"]
        time = request.form["time"]
        time2 = time
        if time == "":
            time2 = 100000 
        ingredient = request.form["ingredient"].strip()
        recipe_search = recipes.search_recipes(
                        "%"+name.lower()+"%",
                        time2,
                        "%"+ingredient.lower()+"%"
                        )
        recipesinfo = [recipes.recipe_properties(x) for x in recipe_search]
        return render_template("search.html", recipes=recipesinfo,
                                name_search=name, maxtime=time, ing_search=ingredient
                )

@app.route("/addreview", methods=["post"])
def addreview():
    users.require_login()
    if request.method == "POST":  
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        recipeinfo = recipes.recipe_properties(recipe_id)
        if recipeinfo[5]: # if recipe is private
            return render_template("error.html", message="Yksityistä reseptiä ei voi arvostella")
        review = request.form["review"]
        grade = request.form["grade"]
        reviews.add_review(user_id, recipe_id, review, grade)
        return redirect("/recipe/"+recipe_id)