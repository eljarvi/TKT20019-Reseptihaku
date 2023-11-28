from db import db
from flask import abort, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def register(username, password, admin=False):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO Users (username, password, admin) VALUES \
                (:username, :hash_value, :admin)"
        db.session.execute(
            text(sql),
            {"username":username, "hash_value": hash_value, "admin": admin}
        )
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, password, admin FROM Users WHERE username = :username"
    user = db.session.execute(text(sql), {"username":username}).fetchone()
    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False
    session["username"] = username
    session["user_id"] = user[0]
    session["user_admin"] = user[2]
    return True

def logout():
    del session["username"]
    del session["user_id"]
    del session["user_admin"]

def check_user(user_id):
    if not "user_id" in session:
        abort(403)
        return
    if user_id != session["user_id"]:
        abort(403)

def require_login():
    if not "user_id" in session:
        abort(403)
