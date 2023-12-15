from db import db
from sqlalchemy.sql import text

def add_favourite(user_id, recipe_id):
    sql = "INSERT INTO Favourites (user_id, recipe_id, visible) \
            VALUES (:user_id, :recipe_id, TRUE)"
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def remove_favourite(user_id, recipe_id):
    sql = "UPDATE Favourites SET visible = FALSE \
            WHERE user_id = :user_id AND recipe_id = :recipe_id"
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def remove_favourites(recipe_id):
    sql = "UPDATE Favourites SET visible = FALSE \
            WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()

def user_favourites(user_id):
    sql = "SELECT recipe_id FROM Favourites F, Recipes R \
            WHERE R.id = F.recipe_id AND F.user_id =:user_id \
            AND F.visible AND R.visible AND not R.privacy"
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return [row[0] for row in result]


def not_favourite(user_id, recipe_id):
    sql = "SELECT COUNT(id) FROM Favourites \
            WHERE user_id = :user_id \
            AND recipe_id = :recipe_id AND visible"
    result = db.session.execute(
                    text(sql),
                    {"user_id": user_id, "recipe_id": recipe_id}
                ).fetchone()[0]
    return result == 0


