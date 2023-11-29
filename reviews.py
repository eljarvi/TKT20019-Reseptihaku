from db import db
from sqlalchemy.sql import text

def add_review(user_id, recipe_id, review, grade):
    sql = "INSERT INTO Reviews (user_id, recipe_id, review, grade, visible) \
            VALUES (:user_id, :recipe_id, :review, :grade, true) RETURNING id"
    db.session.execute(
            text(sql),
            {"user_id": user_id, "recipe_id": recipe_id, "review": review, "grade": grade}
            )
    db.session.commit()
'''
def review_details(review_id):
    sql = "SELECT user_id, recipe_id, review, grade \
            FROM Reviews WHERE id = :review_id AND visible"
    return db.session.execute(text(sql), {"review_id": review_id}).fetchone()
'''

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

def remove_review(user_id, recipe_id):
    sql = "UPDATE Reviews SET visible = false WHERE user_id =:user_id AND recipe_id = :recipe_id"
    db.session.execute(text(sql), {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def remove_reviews(recipe_id):
    sql = "UPDATE Reviews SET visible = false WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()
    