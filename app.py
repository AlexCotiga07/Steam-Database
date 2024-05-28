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
    return render_template("game.html", game=game)


@app.route('/search-results', methods=["get", "post"])
def search():
    item = request.form["search-query"]
    item = f"%{item}%"
    sql = "SELECT id, name FROM Game WHERE name LIKE ?;"
    results = query_db(sql, (item,))
    return render_template("search_results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
