import csv
import sqlite3


def cur_setup():
    """connect to database"""
    conn = sqlite3.connect("steam.db")
    cursor = conn.cursor
    return cursor


def search_game(game):
    """set up stuff for Game table"""
    id = game[0]
    name = game[1]
    date = game[2].replace("/", "-")
    compatables = game[6].split(";")
    if "windows" in compatables:
        windows = 1
    else:
        windows = 0
    if "mac" in compatables:
        mac = 1
    else:
        mac = 0
    if "linux" in compatables:
        linux = 1
    else:
        linux = 0
    minage = game[7]
    achievements = game[11]
    negatives = game[13]
    positives = game[12]
    averagept = game[14]
    medianpt = game[15]
    price = "%.2f" % (float(game[17])*2.08)
    return id, name, date, windows, mac, linux, minage, achievements, negatives, positives, averagept, medianpt, price


def search_genres(game):
    conn = sqlite3.connect("steam.db")
    cursor = cur_setup()
    genres = game[9].split(";")
    for genre in genres:
        cursor.execute("SELECT name FROM Genres WHERE name = ?;" (genre))
        current_genre = cursor.fetchone()
        if not current_genre:
            cursor.execute("INSERT INTO Genre (name) VALUES (?);", (genre))
            conn.commit()


with open("steam.csv", "r", encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile)
    for game in csvreader:
        # if game[0] == "279580":  # for testing
        search_game(game)
        search_genres(game)
