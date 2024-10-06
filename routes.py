from app import app
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import bands
import shows
import songs
import users

@app.route("/")
def index():
    return render_template("index.html", bands=bands.get_all_bands())

@app.route("/test")
def test():
    return render_template("test.html", songs=songs.get_all_songs())

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.login(username, password)

    if not user:
        return render_template("error.html", message="Virheellinen käyttäjätunnus tai salasana")

    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users.register(username, password)
        return redirect("/")

@app.route("/band/<int:id>")
def band(id):
    band = bands.get_band(id)
    band_shows = shows.get_all_band_shows(band.id)
    return render_template("band.html", band=band, shows=band_shows)

@app.route("/addband", methods=["GET", "POST"])
def addband():
    if request.method == "GET":
        return render_template("addband.html")
    
    if request.method == "POST":
        name = request.form["name"]
        band_id = bands.add_band(name)
        return redirect("/")

@app.route("/removeband", methods=["GET", "POST"])
def removeband():
    if request.method == "GET":
        return render_template("removeband.html", bands=bands.get_all_bands())
    
    if request.method == "POST":
        id = int(request.form["bands"])
        bands.remove_band(id)
        return redirect("/")

@app.route("/addsong", methods=["GET", "POST"])
def addsong():
    if request.method == "GET":
        return render_template("addsong.html")
    
    if request.method == "POST":
        name = request.form["name"]
        song_id = songs.add_song(name)
        return redirect("/")


@app.route("/show/<int:id>")
def show(id):
    show = shows.get_show(id)
    show_id = show.id
    venue = shows.get_venue(show.venue_id)
    songs = shows.get_setlist(show_id)
    return render_template("show.html", songs=songs, show=show, venue=venue)

@app.route("/addshow/<band_id>", methods=["GET", "POST"])
def addshow(band_id):

    if request.method == "GET":
       return render_template("addshow.html", venues=shows.get_all_venues(), band_id=band_id)
    
    if request.method == "POST":
        show_name = request.form["name"]
        show_date = request.form["date"]
        venue_name = request.form["venue_name"]

        if venue_name == "":
            venue_id = int(request.form["venues"])
        else:
            address = request.form["venue_address"]
            contact = request.form["venue_contact"]
            venue_id = shows.add_venue(venue_name, address, contact)
        
        show_id = shows.add_show(band_id, show_name, show_date, venue_id)

        return band(band_id)

@app.route("/create_setlist/<show_id>", methods=["GET", "POST"])
def create_setlist(show_id):

    if request.method == "GET":
       return render_template("create_setlist.html", songs=songs.get_all_songs(), show_id=show_id)
    
    if request.method == "POST":
        selected_songs = request.form.getlist("selected_songs")
        for selected_song in selected_songs:
            song = songs.get_song(selected_song)
            setlist_id = shows.add_song_to_setlist(show_id, song.id)

        return show(show_id)