from sqlalchemy.sql import text
from db import db

def get_all_band_shows(band_id):
    sql = text("SELECT id, name, date FROM shows WHERE band_id=:band_id ORDER BY date ASC")
    result = db.session.execute(sql, {"band_id":band_id})
    shows = result.fetchall()
    return shows