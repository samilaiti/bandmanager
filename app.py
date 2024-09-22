from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = text("SELECT id, name, visible FROM bands ORDER by id ASC")
    result = db.session.execute(sql)
    bands = result.fetchall()
    return render_template("index.html", bands=bands)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("error.html", message="Virheellinen käyttäjätunnus")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
        else:
            return render_template("error.html", message="Virheellinen salasana")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return redirect("/")

@app.route("/band/<int:id>")
def band(id):
    sql = text("SELECT id, name FROM bands WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    band = result.fetchone()
    band_id = band.id
    sql = text("SELECT id, name, date FROM shows WHERE band_id=:band_id ORDER BY date ASC")
    result = db.session.execute(sql, {"band_id":band_id})
    shows = result.fetchall()
    return render_template("band.html", band=band, shows=shows)

@app.route("/addband", methods=["GET", "POST"])
def addband():
    if request.method == "GET":
        return render_template("addband.html")
    
    if request.method == "POST":
        name = request.form["name"]
        sql = text(""" INSERT INTO bands (name) 
                   VALUES (:name) RETURNING id """)
        band_id = db.session.execute(sql, {"name":name}).fetchone()[0]
        db.session.commit()
        return redirect("/")

@app.route("/show/<int:id>")
def show(id):
    sql = text("SELECT id, name, date, venue_id FROM shows WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    show = result.fetchone()
    show_id = show.id
    venue_id = show.venue_id
    sql = text("SELECT id, name, address FROM venues WHERE id=:venue_id")
    result = db.session.execute(sql, {"venue_id":venue_id})
    venue = result.fetchone()
    sql = text("SELECT songs.id, songs.name FROM songs, setlist WHERE songs.id = setlist.song_id AND setlist.show_id=:show_id")
    result = db.session.execute(sql, {"show_id":show_id})
    songs = result.fetchall()
    return render_template("show.html", songs=songs, show=show, venue=venue)

@app.route("/addshow/<band_id>", methods=["GET", "POST"])
def addshow(band_id):

    print(band_id)
    if request.method == "GET":
       sql = text("SELECT id, name FROM venues")
       result = db.session.execute(sql)
       venues = result.fetchall()
       return render_template("addshow.html", venues=venues, band_id=band_id)
    
    if request.method == "POST":
        show_name = request.form["name"]
        show_date = request.form["date"]
        venue_name = request.form["venue_name"]

        if venue_name == "":
            venue_id = int(request.form["venues"])
        else:
            address = request.form["venue_address"]
            contact = request.form["venue_contact"]
            sql = text("""INSERT INTO venues (name, address, contact) 
                       VALUES (:venue_name, :address, :contact) RETURNING id """)
            venue_id = db.session.execute(sql, {"venue_name":venue_name, "address":address, "contact":contact}).fetchone()[0]
        
        print(show_date)
        sql = text(""" INSERT INTO shows (name, date, venue_id, band_id) 
                   VALUES (:show_name, :show_date, :venue_id, :band_id) RETURNING id """)
        show_id = db.session.execute(sql, {"show_name":show_name, "show_date":show_date, "venue_id":venue_id, "band_id":band_id}).fetchone()[0]
        db.session.commit()

        return band(band_id)

@app.route("/create_setlist/<show_id>", methods=["GET", "POST"])
def create_setlist(show_id):

    if request.method == "GET":
       sql = text("SELECT id, name FROM songs")
       result = db.session.execute(sql)
       songs = result.fetchall()
       return render_template("create_setlist.html", songs=songs, show_id=show_id)
    
    if request.method == "POST":
        selected_songs = request.form.getlist("selected_songs")
        for song in selected_songs:
            sql = text("SELECT id, name FROM songs WHERE name=:name")
            result = db.session.execute(sql, {"name":song})
            song_id = result.fetchone()[0]
            sql = text(""" INSERT INTO setlist (show_id, song_id) 
                    VALUES (:show_id, :song_id) RETURNING id """)
            setlist_id = db.session.execute(sql, {"show_id":show_id, "song_id":song_id}).fetchone()[0]
            db.session.commit()

        return show(show_id)

    

