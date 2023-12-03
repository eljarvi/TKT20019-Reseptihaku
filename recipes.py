from db import db
from sqlalchemy.sql import text


def add_recipe(user_id, name, desc, time, priv, inst, ingr):
    sql = "INSERT INTO Recipes (user_id, name, description, time, privacy, instruction, visible) \
            VALUES (:user_id, :name, :desc, :time, :priv, :inst, true) RETURNING id"
    recipe_id = db.session.execute(
        text(sql),
        {"user_id": user_id, "name":name, "desc":desc, "time": time, "priv": priv, "inst": inst}
        ).fetchone()[0]

    for ingredient in ingr:
        sql = "INSERT INTO Ingredients (recipe_id, name, quantity, visible) \
            VALUES (:recipe_id, :name, :quantity, true)"
        db.session.execute(
            text(sql),
            {"recipe_id": recipe_id, "name": ingredient[0], "quantity": ingredient[1]}
            )
    db.session.commit()

def add_ingredient(recipe_id, name, quantity):
    sql = "INSERT INTO Ingredients (recipe_id, name, quantity, visible) \
            VALUES (:recipe_id, :name, :quantity, true)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "name": name, "quantity": quantity})
    db.session.commit()

def recipe_properties(recipe_id):
    sql = "SELECT id, user_id, name, description, time, privacy,  \
            instruction FROM Recipes WHERE id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()

def recipe_ingredients(recipe_id):
    sql = "SELECT name, quantity, id FROM Ingredients WHERE recipe_id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()

def users_recipes(user_id):
    sql = "SELECT id FROM Recipes WHERE user_id = :user_id AND visible"
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return [row[0] for row in result]

def all_recipes():
    sql = "SELECT id FROM Recipes WHERE privacy = FALSE AND visible"
    result = db.session.execute(text(sql)).fetchall()
    return [row[0] for row in result]

def remove_recipe(recipe_id):
    sql = "UPDATE Recipes SET visible = FALSE WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    sql = "UPDATE Ingredients SET visible = FALSE WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()

def change_recipe_properties(recipe_id, name, desc, time, priv, inst):
    sql = "UPDATE Recipes SET name = :name, description = :desc, \
            time = :time, privacy = :priv, instruction = :inst \
            WHERE id = :recipe_id"
    db.session.execute(
        text(sql),
        {
        "recipe_id": recipe_id,
        "name": name,
        "desc": desc,
        "time": time,
        "priv": priv,
        "inst": inst
        }
    )
    '''
    sql = "UPDATE Recipes SET description = :desc WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "desc": desc})
    sql = "UPDATE Recipes SET time = :time WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "time": time})
    sql = "UPDATE Recipes SET privacy = :priv WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "priv": priv})
    '''
    db.session.commit()

def remove_ingredient(ingredient_id):
    sql = "UPDATE Ingredients SET visible = false WHERE id =:ingredient_id"
    db.session.execute(text(sql), {"ingredient_id": ingredient_id})
    db.session.commit()

def search_recipes(name, maxtime, ingredient):
    sql = "SELECT DISTINCT R.id FROM Recipes R, Ingredients I \
            WHERE R.id = I.recipe_id AND LOWER(R.name) LIKE :name \
            AND R.time <= :maxtime AND I.visible AND NOT R.privacy \
            AND LOWER(I.name) LIKE :ingredient"
    result = db.session.execute(
            text(sql),
            {"maxtime": maxtime, "name": name, "ingredient": ingredient}
            ).fetchall()
    return [row[0] for row in result]
        