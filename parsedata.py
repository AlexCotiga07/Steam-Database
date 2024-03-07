import csv
import sqlite3


def search_game(game):
    """set up stuff for Game table, put them into the table"""
    conn = sqlite3.connect("steam.db")
    cursor = conn.cursor()
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
    cursor.execute("INSERT INTO Game VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, name, date, windows, mac, linux, minage, achievements, negatives, positives, averagept, medianpt, price,))
    conn.commit()


def search_genres(game):
    """Check if there are any new genres to add, add them,
    and connect genres with game in bridging table"""
    conn = sqlite3.connect("steam.db")
    cursor = conn.cursor()
    genres = game[9].split(";")
    for genre in genres:
        try:
            cursor.execute("SELECT name FROM Genre WHERE name = ?;" (genre,))
        except:  # If not, add the genre in
            cursor.execute("INSERT INTO Genre (name) VALUES (?);", (genre,))
            conn.commit()
        # Add the genre and game ids into bridging table
        cursor.execute("SELECT id FROM Genre WHERE name = ?;", (genre,))
        genre_for_bridging = str(cursor.fetchone())[1:]
        genre_for_bridging = genre_for_bridging[:-1]
        genre_for_bridging = genre_for_bridging[:-1]
        cursor.execute("INSERT INTO GameGenre VALUES (?, ?);", (game[0], genre_for_bridging))
        conn.commit()


with open("steam.csv", "r", encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile)
    for game in csvreader:
        # if game[0] == "279580":  # for testing
        search_game(game)
        search_genres(game)
