from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
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
