from db import db
from sqlalchemy.sql import text

def add_recipe(user_id, name, desc, time, priv):
    sql = "INSERT INTO Recipes (user_id, name, description, time, privacy) \
            VALUES (:user_id, :name, :desc, :time, :priv)"
    db.session.execute(text(sql), {"user_id": user_id, "name":name, "desc":desc, "time": time, "priv": priv})
    db.session.commit()

def add_ingredient(recipe_id, name, quantity, essential):
    sql = "INSERT INTO Ingredients (recipe_id, name, quantity, essential) \
            VALUES (:recipe_id, :name, :quantity, :essential)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "name": name, "quantity": quantity, "essential": essential})
    db.session.commit()

def recipe_properties(recipe_id):
    sql = "SELECT user_id, name, description, time, privacy FROM Recipes WHERE id = :recipe_id"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()

def recipe_ingredients(recipe_id, essential = False):
    if essential:
        sql = "SELECT name, quantity FROM Ingredients WHERE recipe_id = :recipe_id AND essential"
    else:
        sql = "SELECT name, quantity FROM Ingredients WHERE recipe_id = :recipe_id"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()

def recipe_instructions(recipe_id):
    sql = "SELECT instruction FROM Instructions WHERE recipe_id = :recipe_id"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()

def users_recipes(user_id):
    sql = "SELECT id FROM Recipes WHERE user_id = :user_id"
    return db.session.execute(text(sql), {"user_id": user_id}).fetchall()

def all_recipes():
    sql = "SELECT id FROM Recipes WHERE privacy = FALSE"
    return db.session.execute(text(sql)).fetchall()


# add functions to remove and change recipes