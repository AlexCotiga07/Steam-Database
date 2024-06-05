from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from sqlalchemy import true

app = Flask(__name__)

DATABASE = "steam.db"


def query_db(sql, args=(), one=False):
    """Connect and query, to collect data quicker.
    Will return only item if one=True and can accept arguments as a tuple"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, args)  # sql query and stuff that goes in the ?
    results = cursor.fetchall()  # for reading from db
    conn.commit()  # for making changes
    conn.close()
    return (results[0] if results else None) if one else results


@app.route("/")
def browsing():
    results = query_db("SELECT id, name FROM Game ORDER BY name")
    return render_template("index.html", results=results)


@app.route("/game/<int:id>")
def game(id):
    sql = "SELECT * FROM Game WHERE id = ?"
    game = query_db(sql, args=(id,), one=True)
    if game[2][5] == "0" and game[2][6] == "1":  # january
        month = "January"
    elif game[2][5] == "0" and game[2][6] == "2":  # february
        month = "February"
    elif game[2][5] == "0" and game[2][6] == "3":  # march
        month = "March"
    elif game[2][5] == "0" and game[2][6] == "4":  # april
        month = "April"
    elif game[2][5] == "0" and game[2][6] == "5":  # may
        month = "May"
    elif game[2][5] == "0" and game[2][6] == "6":  # june
        month = "June"
    elif game[2][5] == "0" and game[2][6] == "7":  # july
        month = "July"
    elif game[2][5] == "0" and game[2][6] == "8":  # august
        month = "August"
    elif game[2][5] == "0" and game[2][6] == "9":  # september
        month = "September"
    elif game[2][5] == "1" and game[2][6] == "0":  # october
        month = "October"
    elif game[2][5] == "1" and game[2][6] == "1":  # november
        month = "November"
    elif game[2][5] == "1" and game[2][6] == "2":  # december
        month = "December"
    else:
        month = "You messed up"
    sql = "SELECT * FROM Genre \
           JOIN GameGenre \
           ON GameGenre.genreid = Genre.id \
           WHERE GameGenre.gameid = ?"
    genres = query_db(sql, args=(id,))
    sql = "SELECT * FROM Developer \
           JOIN GameDeveloper \
           ON GameDeveloper.devid = Developer.id \
           WHERE GameDeveloper.gameid = ?"
    developers = query_db(sql, args=(id,))
    sql = "SELECT * FROM Publisher \
           JOIN GamePublisher \
           ON GamePublisher.publishid = Publisher.id \
           WHERE GamePublisher.gameid = ?"
    publishers = query_db(sql, args=(id,))
    return render_template("game.html",
                           game=game,
                           genres=genres,
                           developers=developers,
                           publishers=publishers,
                           month=month)


@app.route('/search-results', methods=["get", "post"])
def search():
    item = request.form["search-query"]
    item = f"%{item}%"
    sql = "SELECT id, name FROM Game WHERE name LIKE ?;"
    results = query_db(sql, (item,))
    return render_template("search_results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
