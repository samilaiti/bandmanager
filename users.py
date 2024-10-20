from flask import session, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from db import db
import os
import bands

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    session["csrf_token"] = os.urandom(16).hex()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
        else:
            return False

    return True

def logout():
    del session["username"]
    del session["band_id"]
    del session["band_name"]
    del session["csfr_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return login(username, password)

def select_band(id):
    session["band_id"] = id
    band = bands.get_band(id)
    session["band_name"] = band.name

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
