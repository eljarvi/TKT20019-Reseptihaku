from db import db
from sqlalchemy.sql import text

def add_review(user_id, recipe_id, review, grade):
    sql = "INSERT INTO Reviews (user_id, recipe_id, review, grade, visible) \
            VALUES (:user_id, :recipe_id, :review, :grade, TRUE) RETURNING id"
    db.session.execute(
            text(sql),
            {"user_id": user_id, "recipe_id": recipe_id, "review": review, "grade": grade}
            )
    db.session.commit()

def remove_review(user_id, recipe_id):
    sql = "UPDATE Reviews SET visible = FALSE WHERE user_id =:user_id AND recipe_id = :recipe_id"
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def remove_reviews(recipe_id):
    sql = "UPDATE Reviews SET visible = FALSE WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()

def have_reviewed(user_id, recipe_id):
    sql = "SELECT COUNT(id) FROM Reviews WHERE visible \
            AND user_id = :user_id AND recipe_id = :recipe_id"
    result = db.session.execute(
        text(sql),
        {"user_id": user_id, "recipe_id": recipe_id}
        ).fetchone()[0]
    return result >= 1

def recipe_reviews(recipe_id):
    sql = "SELECT id, user_id, review, grade FROM Reviews \
            WHERE visible AND recipe_id = :recipe_id"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()
