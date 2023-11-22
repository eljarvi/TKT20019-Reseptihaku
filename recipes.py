from db import db
from sqlalchemy.sql import text


def add_recipe(user_id, name, desc, time, priv, ingr, inst):
    sql = "INSERT INTO Recipes (user_id, name, description, time, privacy, visible) \
            VALUES (:user_id, :name, :desc, :time, :priv, true) RETURNING id"
    recipe_id = db.session.execute(text(sql), {"user_id": user_id, "name":name, "desc":desc, "time": time, "priv": priv}).fetchone()[0]
    for ingredient in ingr.strip().split("\n"):
        parts = ingredient.split(";")
        sql = "INSERT INTO Ingredients (recipe_id, name, quantity, visible) \
            VALUES (:recipe_id, :name, :quantity, true)"
        db.session.execute(text(sql), {"recipe_id": recipe_id, "name": parts[0].strip(), "quantity": parts[1].strip()})
    sql = "INSERT INTO Instructions (recipe_id, instruction, visible) \
            VALUES (:recipe_id, :instruction, true)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "instruction": inst})
    db.session.commit()

def add_ingredient(recipe_id, name, quantity):
    sql = "INSERT INTO Ingredients (recipe_id, name, quantity, visible) \
            VALUES (:recipe_id, :name, :quantity, true)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "name": name, "quantity": quantity})
    db.session.commit()

def recipe_properties(recipe_id):
    sql = "SELECT id, user_id, name, description, time, privacy FROM Recipes WHERE id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()

def recipe_ingredients(recipe_id):
    sql = "SELECT name, quantity, id FROM Ingredients WHERE recipe_id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()

def recipe_instructions(recipe_id):
    sql = "SELECT instruction FROM Instructions WHERE recipe_id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()[0]

def users_recipes(user_id):
    sql = "SELECT id FROM Recipes WHERE user_id = :user_id AND visible"
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return [x[0] for x in result]

def all_recipes():
    sql = "SELECT id FROM Recipes WHERE privacy = FALSE AND visible"
    result = db.session.execute(text(sql)).fetchall()
    return [x[0] for x in result]

def remove_recipe(recipe_id):
    sql = "UPDATE Recipes SET visible = FALSE WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    sql = "UPDATE Ingredients SET visible = FALSE WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    sql = "UPDATE Instructions SET visible = FALSE WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()

def change_recipe_properties(recipe_id, name, desc, time, priv):
    sql = "UPDATE Recipes SET name = :name WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "name": name})
    sql = "UPDATE Recipes SET description = :desc WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "desc": desc})
    sql = "UPDATE Recipes SET time = :time WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "time": time})
    sql = "UPDATE Recipes SET privacy = :priv WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "priv": priv})
    db.session.commit()

def change_recipe_instructions(recipe_id, instructions):
    sql = "UPDATE Instructions SET instruction = :instructions WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "instructions": instructions})
    db.session.commit()

def remove_ingredient(ingredient_id):
    sql = "UPDATE Ingredients SET visible = false WHERE id =:ingredient_id"
    db.session.execute(text(sql), {"ingredient_id": ingredient_id})
    db.session.commit()

def search_recipes(name, maxtime, ingredient):
    if maxtime == "":
        maxtime = 10000
    name = "%"+name.lower()+"%"
    sql = "SELECT id FROM Recipes WHERE time <= :maxtime AND LOWER(name) LIKE :name AND visible"
    results1 = [x[0] for x in db.session.execute(text(sql), {"maxtime": maxtime, "name": name}).fetchall()]
    ingredient = "%" + ingredient + "%"
    sql = "SELECT recipe_id FROM Ingredients WHERE LOWER(name) LIKE :ingredient AND visible"
    results2 = [x[0] for x in db.session.execute(text(sql), {"ingredient": ingredient})]
    return list(set(results1) & set(results2)) 



