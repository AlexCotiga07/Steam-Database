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

    # Turn month into a word
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

    # System compatability
    # The variables are used to change the class of the text
    # so if it's not compatible the text won't show
    if game[3] == 1:
        windows = "compatible"
    else:
        windows = "not-compatible"
    if game[4] == 1:
        mac = "compatible"
    else:
        mac = "not-compatible"
    if game[5] == 1:
        linux = "compatible"
    else:
        linux = "not-compatible"

    # Popularity (% liked)
    percent_rating = "%.1f" % (100*(game[9]/(game[8]+game[9])))

    # Age rating
    # The variables are used to change the class of the text
    # so if it's not restricted the text won't show
    if game[6] == 0:
        age_restrict = "any-age"
    else:
        age_restrict = "age_restricted"

    # Playtime
    if game[10] == 0:
        average_pt = "Unavailable"
    else:
        average_pt = f"{game[10]} hours"
    if game[11] == 0:
        median_pt = "Unavailable"
    else:
        median_pt = f"{game[11]} hours"

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
                           month=month,
                           windows=windows,
                           mac=mac,
                           linux=linux,
                           percent_rating=percent_rating,
                           age_restrict=age_restrict,
                           average_pt=average_pt,
                           median_pt=median_pt)


@app.route('/search-results', methods=["get", "post"])
def search():
    item = request.form["search-query"]
    item = f"%{item}%"
    sql = "SELECT id, name FROM Game WHERE name LIKE ?;"
    results = query_db(sql, (item,))
    return render_template("search_results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
