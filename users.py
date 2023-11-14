from db import db
from flask import session
from sqlalchemy.sql import text

# TODO: improve security

def register(username, password, admin=False):
    try:
        sql = "INSERT INTO Users (username, password, admin) VALUES \
                (:username, :password, :admin)"
        db.session.execute(text(sql), {"username":username, "password":password, "admin": admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, password, admin FROM Users WHERE username = :username"
    user = db.session.execute(text(sql), {"username":username}).fetchone()
    if not user:
        return False
    if password != user[1]:
        return False
    session["username"] = username
    session["user_id"] = user[0]
    session["user_admin"] = user[2]
    return True

def logout():
    del session["username"]
    del session["user_id"]
    del session["user_admin"]

