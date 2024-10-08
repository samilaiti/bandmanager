from sqlalchemy.sql import text
from db import db

def get_all_band_shows(band_id):
    sql = text("SELECT id, name, date FROM shows WHERE band_id=:band_id ORDER BY date ASC")
    result = db.session.execute(sql, {"band_id":band_id})
    shows = result.fetchall()
    return shows

def get_show(id):
    sql = text("SELECT id, name, date, venue_id FROM shows WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    show = result.fetchone()
    return show

def add_show(band_id, show_name, show_date, venue_id):
    sql = text(""" INSERT INTO shows (name, date, venue_id, band_id) 
                VALUES (:show_name, :show_date, :venue_id, :band_id) RETURNING id """)
    show_id = db.session.execute(sql, {"show_name":show_name, "show_date":show_date, "venue_id":venue_id, "band_id":band_id}).fetchone()[0]
    db.session.commit()
    return show_id

def get_all_venues():
    sql = text("SELECT id, name FROM venues")
    result = db.session.execute(sql)
    venues = result.fetchall()
    return venues

def get_venue(id):
    sql = text("SELECT id, name, address FROM venues WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    venue = result.fetchone()
    return venue

def add_venue(venue_name, address, contact):
    sql = text("""INSERT INTO venues (name, address, contact) 
                VALUES (:venue_name, :address, :contact) RETURNING id """)
    venue_id = db.session.execute(sql, {"venue_name":venue_name, "address":address, "contact":contact}).fetchone()[0]
    return venue_id

def get_setlist(show_id):
    sql = text("SELECT songs.id, songs.name FROM songs, setlist WHERE songs.id = setlist.song_id AND setlist.show_id=:show_id")
    result = db.session.execute(sql, {"show_id":show_id})
    songs = result.fetchall()
    return songs

def add_song_to_setlist(show_id, song_id):
    sql = text(""" INSERT INTO setlist (show_id, song_id) 
            VALUES (:show_id, :song_id) RETURNING id """)
    setlist_id = db.session.execute(sql, {"show_id":show_id, "song_id":song_id}).fetchone()[0]
    db.session.commit()
    return setlist_id


