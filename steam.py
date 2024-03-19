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
                           price, \
                           id \
                    FROM Game \
                    WHERE id = ?;", (id,))
    game_data = cursor.fetchone()

    # Printing data
    # Name, release date, percentage
    percent_rating = "%.1f" % (100*(game_data[8]/(game_data[8]+game_data[7])))
    print()
    print("-"*30)
    print(f"{game_data[0]}   {percent_rating}%")
    print(f"Release date (yyyy/mm/dd): {game_data[1]}")

    # Minimum age
    if game_data[5] > 0:  # Only print if age restricited
        print(f"R{game_data[5]}")

    # Available achievements
    print(f"{game_data[6]} achievements available")

    # Price
    if game_data[11] == 0:
        print("FREE")
    else:
        print(f"${game_data[11]}")

    print()

    # Compatable systems
    compats = []  # Storing compatable systems
    if game_data[2] == 1:  # Check windows compatability
        compats.append("Windows")
    if game_data[3] == 1:  # Check mac compatability
        compats.append("Mac")
    if game_data[4] == 1:  # Check linux compatability
        compats.append("Linux")
    print("Compatable systems:")
    for system in compats:
        print(system)

    print()

    # Average and median playtimes
    if game_data[9] == 0:
        print("Average playtime unavailable")
    else:
        print(f"Average playtime: {game_data[9]} hours")
    if game_data[10] == 0:
        print("Median playtime unavailable")
    else:
        print(f"Median playtime: {game_data[10]} hours")

    # print(game_data)
    conn.close()  # Close connection to save efficiency


if __name__ == "__main__":
    while True:
        read = input("Id of game: ")
        read_one(read)
        break
