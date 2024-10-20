from app import app
from flask import redirect, render_template, request, session
import bands
import shows
import songs
import users
import json

@app.route("/")
def index():
    session["bands"] = []
    all_bands = bands.get_all_bands()
    for band in all_bands:
        session["bands"].extend([(band.id, band.name)])
    print(session["bands"])
    return render_template("index.html", bands=bands.get_all_bands())

@app.route("/select_band", methods=["POST"])
def select_band():
    band_id = int(request.form["bands"])
    users.select_band(band_id)
    return redirect("/")

@app.route("/login",methods=["POST", "GET"])
def login():

    if (request.method == "GET"):
        return render_template("login.html")
    
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

@app.route("/band/")
def band_missing():
    return render_template("error.html", message="Valitse bändi ylävalikosta", message_style="info")

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
        users.check_csrf()
        name = request.form["name"]

        if name == "":
            return render_template("error.html", message="Bändin nimi ei voi olla tyhjä", message_style="info")
        
        try:
            band_id = bands.add_band(name)
            return redirect("/")
        except Exception as error:
            return render_template("error.html", message=error, message_style="danger")

@app.route("/removeband", methods=["GET", "POST"])
def removeband():
    if request.method == "GET":
        return render_template("removeband.html", bands=bands.get_all_bands())
    
    if request.method == "POST":
        users.check_csrf()
        id = int(request.form["bands"])
        bands.remove_band(id)
        return redirect("/")

@app.route("/addsong", methods=["GET", "POST"])
def addsong():
    if request.method == "GET":
        return render_template("addsong.html")
    
    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]

        if name == "":
            return render_template("error.html", message="Biisin nimi ei voi olla tyhjä", message_style="info")
        
        try:
            song_id = songs.add_song(name)
            return redirect("/")
        except Exception as error:
            return render_template("error.html", message=error, message_style="danger")


@app.route("/show/<int:id>")
def show(id):
    show = shows.get_show(id)
    show_id = show.id
    venue = shows.get_venue(show.venue_id)
    songs = shows.get_setlist(show_id)
    return render_template("show.html", songs=songs, show=show, venue=venue)

@app.route("/addshow/")
def band_show_missing():
    return render_template("error.html", message="Valitse bändi ylävalikosta", message_style="info")

@app.route("/addshow/<band_id>", methods=["GET", "POST"])
def addshow(band_id):

    if request.method == "GET":
       return render_template("addshow.html", venues=shows.get_all_venues(), band_id=band_id)
    
    if request.method == "POST":
        users.check_csrf()
        show_name = request.form["name"]
        show_date = request.form["date"]
        venue_name = request.form["venue_name"]

        if show_name == "":
            return render_template("error.html", message="Keikan nimi ei voi olla tyhjä", message_style="info")

        if show_date == "":
            return render_template("error.html", message="Päivämäärä ei voi olla tyhjä", message_style="info")

        if venue_name == "":
            venue_id = int(request.form["venues"])
        else:
            address = request.form["venue_address"]

            if address == "":
                return render_template("error.html", message="Osoite ei voi olla tyhjä", message_style="info")            

            contact = request.form["venue_contact"]
            venue_id = shows.add_venue(venue_name, address, contact)
        
        show_id = shows.add_show(band_id, show_name, show_date, venue_id)

        return redirect("/")

@app.route("/create_setlist/<band_id>", methods=["GET", "POST"])
def create_setlist(band_id):

    if request.method == "GET":
       return render_template("create_setlist.html", shows=shows.get_band_shows_with_empty_setlist(int(band_id)), songs=songs.get_all_songs())    
    
    if request.method == "POST":
        users.check_csrf()
        show_id = int(request.form["selected_shows"])
        print("routes:", show_id)
        shows.save_setlist(show_id)

        return redirect("/")
    
@app.route("/allsongs")
def allsongs():    
    return render_template("allsongs.html", all_songs=songs.get_all_songs())

@app.route("/process", methods=["POST"])
def process():
    data = json.loads(request.data)
    sl = shows.process_setlist(data)
    print(sl)

    result = "ok"
    return result
