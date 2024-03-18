import sqlite3


def read_one(id):
    """Display all data for a specified game by id"""
    # Connect to database
    conn = sqlite3.connect("steam.db")
    cursor = conn.cursor()
    # Collect data from game table
    cursor.execute("SELECT name, \
                           releasedate, \
                           windowscompat, \
                           maccompat, \
                           linuxcompat, \
                           minage, \
                           achievments, \
                           negreviews, \
                           posreviews, \
                           averageplaytime, \
                           medianplaytime, \
                           price \
                    FROM Game \
                    WHERE id = ?;", (id,))
    game_data = cursor.fetchone()
    print(game_data)
    conn.close()  # Close connection to save efficiency


if __name__ == "__main__":
    while True:
        read = input("Id of game: ")
        read_one(read)
        break
