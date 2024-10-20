from sqlalchemy.sql import text
from db import db

def get_all_songs():
    sql = text("SELECT id, name, visible FROM songs")
    result = db.session.execute(sql)
    songs = result.fetchall()
    return songs

def get_song(name):
    sql = text("SELECT id, name FROM songs WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    song = result.fetchone()
    return song

def add_song(name):
    sql = text(""" INSERT INTO songs (name) 
            VALUES (:name) RETURNING id """)
    song_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    db.session.commit()
    return song_id

def number_of_songs():
    sql = text("SELECT COUNT(*) FROM songs")
    result = db.session.execute(sql)
    num_of_songs = result.fetchone()[0]
    return num_of_songs

