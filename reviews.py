from db import db
from sqlalchemy.sql import text

def add_review(user_id, recipe_id, review, grade):
    sql = "INSERT INTO Reviews (user_id, recipe_id, review, grade, visible) \
            VALUES (:user_id, :recipe_id, :review, :grade, true) RETURNING id"
    review_id = db.session.execute(
                text(sql),
                {"user_id": user_id, "recipe_id": recipe_id, "review": review, "grade": grade}
                ).fetchone()[0]
    return review_id

def review_details(review_id):
    sql = "SELECT user_id, recipe_id, review, grade \
            FROM Reviews WHERE id = :review_id AND visible"
    return db.session.execute(text(sql), {"review_id": review_id}).fetchone()
