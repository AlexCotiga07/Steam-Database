import sqlite3

DATABASE = "steam.db"
# game_ids = []
# game = []

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('SELECT * FROM Game WHERE name LIKE "%hentai%";')
game_ids = cursor.fetchall()

for game in game_ids:
    print(game[0])
    # game = f"'{game[0]}'"
    cursor.execute("DELETE FROM GameDeveloper WHERE gameid = ?;", (game[0],))
    conn.commit()
    cursor.execute("DELETE FROM GamePublisher WHERE gameid = ?;", (game[0],))
    conn.commit()
    cursor.execute("DELETE FROM GameGenre WHERE gameid = ?;", (game[0],))
    conn.commit()
    cursor.execute("DELETE FROM Game WHERE id = ?;", (game[0],))
    conn.commit()
