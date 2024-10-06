from sqlalchemy.sql import text
from db import db

def get_all_bands():
    sql = text("SELECT id, name, visible FROM bands ORDER by id ASC")
    result = db.session.execute(sql)
    bands = result.fetchall()
    return bands

def get_band(id):
    sql = text("SELECT id, name FROM bands WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    band = result.fetchone()
    return band

def add_band(name):
    sql = text(""" INSERT INTO bands (name) 
                VALUES (:name) RETURNING id """)
    band_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    db.session.commit()
    return band_id

def remove_band(id):
    sql = text("UPDATE bands SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

