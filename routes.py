from flask import render_template, request, redirect
from app import app
import recipes
import users
import reviews
import favourites

@app.route("/")
def index():
    return render_template("index.html", recipes_count=len(recipes.all_recipes()))

@app.route("/login", methods=['post', 'get'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if users.login(user, password):
            return redirect("/")
        return render_template("error.html", message="Salasana tai käyttäjätunnus virheellinen.")

@app.route("/register", methods=['post', 'get'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"].strip()
        if len(username) < 1 or len(username) >20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä. "+
                                                        "Välilyöntejä ei lasketa merkeiksi.")
        password1 = request.form["password1"].strip()
        password2 = request.form["password2"].strip()
        if len(password1) < 5 or len(password1)>50:
            return render_template("error.html", message="Salasanassa tulee olla 5-50 merkkiä. " +
                                                        "Välilyöntejä ei lasketa merkeiksi.")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat.")
        if users.register(username, password1):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut. " +
                                                    "Kokeile toista käyttäjänimeä.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/myrecipes/<int:user_id>")
def myrecipes(user_id):
    users.check_user(user_id)
    user_recipes = recipes.users_recipes(user_id)
    fav_ids = favourites.user_favourites(user_id)
    favs = [recipes.recipe_properties(id) for id in fav_ids]
    return render_template("myrecipes.html", recipes=user_recipes, favourites=favs)

@app.route("/addrecipe", methods=["post", "get"])
def add_recipe():
    if request.method == "GET":
        users.require_login()
        return render_template("addrecipe.html")
    if request.method == "POST":
        users.check_csrf()
        user = request.form["user_id"]
        users.check_user(int(user))
        name = request.form["name"].strip()
        if len(name) <1 or len(name) > 50:
            return render_template("error.html", message="Nimen tulee olla 1-50 merkkiä."+
                                                        "Välilyöntejä ei lasketa merkeiksi.")
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
                         message="Raaka-aineet on syötettävä muodossa "+
                                "raaka-aine;määrä ja erotettava rivinvaihdolla.\n" +
                                "Jos et halua lisätä määrää kirjoita muodossa raaka-aine; . " +
                                "Raaka-ainekenttä ei voi olla tyhjä."
                        )
        inst = request.form["instructions"]
        priv = request.form["privacy"]
        recipes.add_recipe(user, name, desc, time, priv, inst, ingr)
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
        parameters = {
            "recipe_id" : recipe_id,
            "owner_id" : recipeinfo[1],
            "name" : recipeinfo[2],
            "description" : recipeinfo[3],
            "time": time,
            "ingredients" : ingr,
            "priv": recipeinfo[5],
            "instruction" : recipeinfo[6],
            "reviewed": reviews.have_reviewed(users.get_user(), recipe_id),
            "reviews": reviews.recipe_reviews(recipe_id),
            "not_favourite": favourites.not_favourite(users.get_user(), recipe_id)
        }
        return render_template("recipe.html", **parameters)

@app.route("/delete", methods=["post"])
def delete():
    if request.method == "POST":
        users.check_csrf()
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        admin = request.form["admin"]
        if admin.lower() =="true":
            users.require_admin()
        recipe_id = request.form["recipe_id"]
        recipes.remove_recipe(recipe_id)
        reviews.remove_reviews(recipe_id)
        favourites.remove_favourites(recipe_id)
        if admin.lower() == "true":
            return redirect("/search")
        return redirect("/myrecipes/"+user_id)

@app.route("/modify", methods=["post"])
def modify():
    if request.method == "POST":
        users.check_csrf()
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        recipeinfo = recipes.recipe_properties(recipe_id)
        ingr = recipes.recipe_ingredients(recipe_id)
        parameters = {
            "id": recipe_id,
            "name": recipeinfo[2],
            "desc": recipeinfo[3],
            "time": recipeinfo[4],
            "priv": recipeinfo[5],
            "ingredients": ingr,
            "instructions": recipeinfo[6]
        }
        return render_template("modify.html", **parameters)

@app.route("/savechanges", methods=["post"])
def save_changes():
    if request.method == "POST":
        users.check_csrf()
        recipe_id = request.form["recipe_id"]
        owner_id = recipes.recipe_properties(recipe_id)[1]
        users.check_user(owner_id)
        new_name = request.form["name"].strip()
        if len(new_name) < 1 or len(new_name) > 50:
            return render_template("error.html", message="Nimen tulee olla 1-50 merkkiä."+
                                                        "Välilyöntejä ei lasketa merkeiksi.")
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
                        message="Raaka-aineet on syötettävä omille" +
                                    "riveilleen muodossa raaka-aine;määrä.\n" +
                                    "Jos et halua lisätä määrää kirjoita muodossa raaka-aine; ."
                            )

        removed = request.form.getlist("removed")
        for ing in removed:
            recipes.remove_ingredient(ing)

        recipes.change_recipe_properties(recipe_id, new_name, new_desc, new_time, new_priv, new_inst)

    return redirect("/recipe/"+recipe_id)

@app.route("/search", methods=["post", "get"])
def search():
    if request.method == "GET":
        recipesinfo = recipes.all_recipes()
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
def add_review():
    users.require_login()
    if request.method == "POST":
        users.check_csrf()  
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

@app.route("/deletereview", methods=["post"])
def delete_review():
    if request.method == "POST":
        users.check_csrf()
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        admin = request.form["admin"]
        review_user = request.form["review_user"]
        if admin.lower() == "true":
            users.require_admin()
        else:
            users.check_user(int(review_user)) 
        reviews.remove_review(review_user, recipe_id)
        return redirect("/recipe/"+recipe_id)

@app.route("/addfavourite", methods=["post"])
def add_favourite():
    if request.method == "POST":
        users.check_csrf()
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        recipeinfo = recipes.recipe_properties(recipe_id)
        if recipeinfo[5]: #if the recipe is private
            users.check_user(int(recipeinfo[1])) # check if the user is the recipe's owner
        if favourites.not_favourite(user_id, recipe_id):
            favourites.add_favourite(user_id, recipe_id)
        return redirect("/recipe/"+recipe_id)

@app.route("/deletefavourite", methods=["post"])
def delete_favourite():
    if request.method == "POST":
        users.check_csrf()
        user_id = request.form["user_id"]
        users.check_user(int(user_id))
        recipe_id = request.form["recipe_id"]
        favourites.remove_favourite(user_id, recipe_id)
        return redirect("/recipe/"+recipe_id)
