from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from sqlalchemy import true
import math
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# key needed for sessions and flash messages
app.config['SECRET_KEY'] = "AlexIsTheBest"

STEAM_DATABASE = "steam.db"
ACCOUNT_DATABASE = "accounts.db"
LIMIT = 50


def query_db(sql, args=(), one=False):
    """Connect and query, to collect data quicker.
    Will return one item if one=True and can accept arguments as a tuple"""
    conn = sqlite3.connect(STEAM_DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, args)  # sql query and stuff that goes in the ?
    results = cursor.fetchall()  # for reading from db
    conn.commit()  # for making changes
    conn.close()
    return (results[0] if results else None) if one else results


@app.route("/")
def landing():
    return redirect("/browsing/1")


@app.route("/browsing/<int:page>")
def browsing(page):
    offset = (page-1)*LIMIT
    rows = query_db("SELECT COUNT(name) FROM Game")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            ORDER BY name LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("index.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/game/<int:id>", methods=["GET","POST"])
def game(id):
    sql = "SELECT * FROM Game WHERE id = ?"
    game = query_db(sql, args=(id,), one=True)

    if not game:
        return render_template("empty_page.html")
    else:
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

        # price
        if game[12] == 0:
            price = "FREE"
        else:
            if str(game[12])[-2] == ".":
                price = f"NZ${game[12]}0"
            else:
                price = f"NZ${game[12]}"

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
            age_restrict = "visible"

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

        # check if game is already on dashboard
        if "user" in session:
            if session["user"] != None:
                sql = "SELECT * FROM UserGame WHERE gameid = ? AND userid = ?"
                is_it_here = query_db(sql, (id, session["user"][0]), one=True)
                if is_it_here:
                    added = True
                else:
                    added = False
            else:
                added = False
        else:
            added = False

        return render_template("game.html",
                               game=game,
                               genres=genres,
                               developers=developers,
                               publishers=publishers,
                               month=month,
                               price=price,
                               windows=windows,
                               mac=mac,
                               linux=linux,
                               percent_rating=percent_rating,
                               age_restrict=age_restrict,
                               average_pt=average_pt,
                               median_pt=median_pt,
                               id=id,
                               added=added)


@app.route('/search-results', methods=["get", "post"])
def search():
    item = request.form["search-query"]
    itemm = f"%{item}%"
    sql = "SELECT id, name FROM Game WHERE name LIKE ? ORDER BY name LIMIT ?;"
    results = query_db(sql, (itemm, LIMIT))
    if not results:
        return render_template("empty_search.html", item=item)
    else:
        return render_template("search_results.html", results=results, item=item)


@app.errorhandler(404)
def page_not_found_404(e):
    return render_template("404.html"), 404


@app.route("/most_played/<int:page>")
def most_played(page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(name) FROM Game")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            ORDER BY medianplaytime DESC\
                            LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("most_played.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/free_games/<int:page>")
def free_games(page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(name) FROM Game WHERE price = 0")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            WHERE price = 0 \
                            ORDER BY name LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("free_games.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/highest_rated/<int:page>")
def highest_rated(page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(name) FROM Game WHERE negreviews > 0 AND posreviews > 0")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            WHERE negreviews > 0 AND posreviews > 0 \
                            ORDER BY (10000 * posreviews / (posreviews + negreviews)) DESC \
                            LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("highest_rated.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/genre_browsing/<int:id>/<int:page>")
def genre_browsing(id, page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(Game.name) FROM Game JOIN GameGenre ON Game.id = GameGenre.gameid WHERE GameGenre.genreid = ?", (id,))
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        genre = query_db("SELECT name FROM Genre WHERE id = ?", (id,))
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT Game.id, Game.name \
                            FROM Game \
                            JOIN GameGenre ON Game.id = GameGenre.gameid \
                            WHERE GameGenre.genreid = ? \
                            ORDER BY Game.name \
                            LIMIT ? OFFSET ?",
                           (id, LIMIT, offset))
        return render_template("genre_browsing.html",
                               results=results,
                               id=id,
                               genre=genre,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/dev_browsing/<int:id>/<int:page>")
def dev_browsing(id, page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(Game.name) FROM Game JOIN GameDeveloper ON Game.id = GameDeveloper.gameid WHERE GameDeveloper.devid = ?", (id,))
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        dev = query_db("SELECT name FROM Developer WHERE id = ?", (id,))
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT Game.id, Game.name \
                            FROM Game \
                            JOIN GameDeveloper ON Game.id = GameDeveloper.gameid \
                            WHERE GameDeveloper.devid = ? \
                            ORDER BY Game.name \
                            LIMIT ? OFFSET ?",
                           (id, LIMIT, offset))
        return render_template("dev_browsing.html",
                               results=results,
                               id=id,
                               dev=dev,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/publisher_browsing/<int:id>/<int:page>")
def publisher_browsing(id, page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(Game.name) FROM Game JOIN GamePublisher ON Game.id = GamePublisher.gameid WHERE GamePublisher.publishid = ?", (id,))
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        publisher = query_db("SELECT name FROM Publisher WHERE id = ?", (id,))
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT Game.id, Game.name \
                            FROM Game \
                            JOIN GamePublisher ON Game.id = GamePublisher.gameid \
                            WHERE GamePublisher.publishid = ? \
                            ORDER BY Game.name \
                            LIMIT ? OFFSET ?",
                           (id, LIMIT, offset))
        return render_template("publisher_browsing.html",
                               results=results,
                               id=id,
                               publisher=publisher,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/windows/<int:page>")
def windows_browsing(page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(name) FROM Game WHERE windowscompat = 1")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            WHERE windowscompat = 1 \
                            ORDER BY name \
                            LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("windows.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/mac/<int:page>")
def mac_browsing(page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(name) FROM Game WHERE maccompat = 1")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            WHERE maccompat = 1 \
                            ORDER BY name \
                            LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("mac.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/linux/<int:page>")
def linux_browsing(page):
    offset = (page-1)*LIMIT
    # page organising
    rows = query_db("SELECT COUNT(name) FROM Game WHERE linuxcompat = 1")
    if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
        return render_template("404.html")
    else:
        if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
            previous = "hide"
            next_page = "hide"
        elif page == 1:
            previous = "hide"
            next_page = "next-page"
        elif page == (math.ceil(int(rows[0][0])/LIMIT)):
            previous = "previous-page"
            next_page = "hide"
        else:
            previous = "previous-page"
            next_page = "next-page"
        results = query_db("SELECT id, name \
                            FROM Game \
                            WHERE linuxcompat = 1 \
                            ORDER BY name \
                            LIMIT ? OFFSET ?",
                           (LIMIT, offset))
        return render_template("linux.html",
                               results=results,
                               page=page,
                               previous=previous,
                               next_page=next_page)


@app.route("/signin", methods=["GET","POST"])
def signin():
    # if the user posts a username and password
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # try to find this user in the database
        sql = "SELECT * FROM User WHERE username = ?"
        user = query_db(sql=sql,args=(username,),one=True)
        if user:
            # there is a user, check password matches
            if check_password_hash(user[2],password):
                # correct password, store username in session
                session["user"] = user
                flash(f"Welcome {username}")
            else:
                flash("Password incorrect")
        else:
            flash("Username does not exist")
    return render_template("login.html")


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        # add new username and password to database
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        # check if username or password are too long or short (or nonexistent)
        if len(username) < 5 or len(username) > 20:
            flash("Username must be between 5 and 20 characters long")
        elif len(password) < 5 or len(password) > 20:
            flash("Password must be between 5 and 20 characters long")
        elif password != password2:
            flash("Passwords don't match")
        else:
            # chack if username already exists
            sql = "SELECT username FROM User WHERE username = ?"
            exists = query_db(sql, args=(username,), one=True)
            if exists:
                flash("Username already exists")
            else:
                # hash the password
                hashed_password = generate_password_hash(password)
                # insert it
                sql = "INSERT INTO User (username,password,adminaccess) VALUES (?,?,0)"
                query_db(sql,(username,hashed_password))
                # collect the data to have id as well
                sql = "SELECT * FROM User WHERE username = ?"
                user = query_db(sql=sql,args=(username,),one=True)
                session["user"] = user
                flash("Sign up successful")
                return redirect("/dashboard/1")
    return render_template("signup.html")


@app.route("/signout")
def signout():
    session["user"] = None
    return redirect("/browsing/1")


@app.route("/dashboard/<int:page>")
def dashboard(page):
    if "user" not in session or session["user"] == None:
        return redirect("/signin")
    else:
        user = session["user"]
        user_id = user[0]
        rows = query_db("SELECT COUNT(Game.name) FROM Game \
                        JOIN UserGame ON Game.id = UserGame.gameid \
                        JOIN User ON UserGame.userid = User.id \
                        WHERE UserGame.userid = ?",(user_id,))
        if rows[0][0] > 0:  # Check if there are actually any games
            if page < 1 or page > (math.ceil(int(rows[0][0])/LIMIT)):
                return render_template("404.html")
            else:
                favourites = "favs"
                offset = (page-1)*LIMIT
                if (math.ceil(int(rows[0][0])/LIMIT)) == 1:
                    previous = "hide"
                    next_page = "hide"
                elif page == 1:
                    previous = "hide"
                    next_page = "next-page"
                elif page == (math.ceil(int(rows[0][0])/LIMIT)):
                    previous = "previous-page"
                    next_page = "hide"
                else:
                    previous = "previous-page"
                    next_page = "next-page"
                results = query_db("SELECT Game.id, Game.name \
                                    FROM Game \
                                    JOIN UserGame ON Game.id = UserGame.gameid \
                                    WHERE UserGame.userid = ? \
                                    ORDER BY Game.name \
                                    LIMIT ? OFFSET ?",
                                (user_id, LIMIT, offset))
                return render_template("dashboard.html",
                                        results=results,
                                        page=page,
                                        previous=previous,
                                        next_page=next_page,
                                        username=user[1],
                                        favourites=favourites)
        else:  # No games saved by this person
            previous = "hide"
            next_page = "hide"
            favourites = "no-favs"
            results = None
            return render_template("dashboard.html",
                                    results=results,
                                    page=page,
                                    previous=previous,
                                    next_page=next_page,
                                    username=user[1],
                                    favourites=favourites)


@app.route("/add_to_dash/<int:game_id>", methods=["POST","GET"])
def add_to_dash(game_id):
    if request.method == "POST":
        if "user" not in session or session["user"] == None:
            return redirect("/signin")
        else:
            username = session["user"]
            sql = "SELECT id FROM User WHERE username = ?"
            user_id = query_db(sql,args=(username[1],),one=True)
            sql = "INSERT INTO UserGame (gameid, userid) VALUES (?,?)"
            query_db(sql,args=(game_id,user_id[0]))
            flash = "Added to list"
    return redirect(f"/game/{game_id}")
    


@app.route("/remove_from_dash/<int:game_id>", methods=["POST","GET"])
def remove_from_dash(game_id):
    if request.method == "POST":
        username = session["user"]
        sql = "SELECT id FROM User WHERE username = ?"
        user_id = query_db(sql,args=(username[1],),one=True)
        sql = "DELETE FROM UserGame WHERE gameid = ? AND userid = ?"
        query_db(sql,args=(game_id,user_id[0]))
    return redirect(f"/game/{game_id}")


@app.route("/credits")
def credits():
    return render_template("credits.html")


@app.route("/terms_of_use")
def terms_of_use():
    return render_template("terms.html")


if __name__ == "__main__":
    app.run(debug=True)
