import sqlite3
import math

DATABASE_FILE = "steam.db"
ITEMS_PER_PAGE = 40


def read_one(id):
    """Display all data for a specified game by id"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
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
    # Genre collection
    cursor.execute("SELECT Genre.name \
                    FROM Genre \
                        JOIN GameGenre ON GameGenre.genreid = Genre.id \
                    WHERE GameGenre.gameid = ?;", (id,))
    genre_data = cursor.fetchall()
    # Dev collection
    cursor.execute("SELECT Developer.name \
                    FROM Developer \
                        JOIN GameDeveloper ON GameDeveloper.devid = Developer.id \
                    WHERE GameDeveloper.gameid = ?;", (id,))
    dev_data = cursor.fetchall()
    # Publisher collection
    cursor.execute("SELECT Publisher.name \
                    FROM Publisher \
                        JOIN GamePublisher ON GamePublisher.publishid = Publisher.id \
                    WHERE GamePublisher.gameid =?;", (id,))
    publisher_data = cursor.fetchall()

    # Printing data
    # Name, release date, percentage
    percent_rating = "%.1f" % (100*(game_data[8]/(game_data[8]+game_data[7])))
    print()
    print("-"*30)
    print(f"{game_data[0]}   {percent_rating}%")
    print(f"Release date (yyyy-mm-dd): {game_data[1]}")

    # Minimum age
    if game_data[5] > 0:  # Only print if age restricited
        print(f"R{game_data[5]}")

    # Available achievements
    print(f"{game_data[6]} achievements available")

    # Price
    if game_data[11] == 0:
        print("FREE")
    else:
        if str(game_data[11])[-2] == ".":
            price = str(game_data[11]) + "0"
            print(f"${price}")
        else:
            print(f"${game_data[11]}")

    print()

    # Genres
    print("Genres:")
    for genre in genre_data:
        print(genre[0])

    print()

    # Developers
    print("Developers:")
    for dev in dev_data:
        print(dev[0])

    print()

    # Publishers
    print("Publishers:")
    for publisher in publisher_data:
        print(publisher[0])

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

    print("-"*30)
    conn.close()  # Close connection to save efficiency


def show_genres():
    """Show list of all genres"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * \
                    FROM Genre \
                    ORDER BY name;")
    genres = cursor.fetchall()

    # Print the genres in a block
    print("-"*35)
    print(f"| {'ID':<4} | Genre")
    print("-"*35)
    for genre in genres:
        print(f"| {genre[0]:<4} | {genre[1]}")
    print("-"*35)

    conn.close()  # Close connection to save efficiency


def show_developers():
    """Show list of all developers"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * \
                    FROM Developer \
                    ORDER BY name;")
    developers = cursor.fetchall()

    page = 1  # Because there's a lot of devs
    max_pages = math.ceil((len(developers))/ITEMS_PER_PAGE)
    continuing = True
    while continuing is True:
        amounts_min = (page-1)*ITEMS_PER_PAGE
        dev_list = []
        for i in range(ITEMS_PER_PAGE):  # Just look at these of an amount
            dev_list.append(developers[amounts_min])
            amounts_min = amounts_min + 1
        # Print the developers in a block
        print("-"*36)
        print(f"| {'ID':<5} | Developer")
        print("-"*36)
        for dev in dev_list:
            print(f"| {dev[0]:<5} | {dev[1]}")
        print("-"*36)

        # Page switching
        if page == 1:
            while True:
                next = input("Type NEXT for next page, END to retrun to menu: ")
                if next == "NEXT":
                    page = page + 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")
        elif page == max_pages:
            while True:
                next = input("Type BACK for previous page, END to retrun to menu: ")
                if next == "BACK":
                    page = page - 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")
        else:
            while True:
                next = input("Type NEXT for next page, BACK for previous page, END to retrun to menu: ")
                if next == "NEXT":
                    page = page + 1
                    break
                elif next == "BACK":
                    page = page - 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")

    conn.close()  # Close connection to save efficiency


def show_publishers():
    """Show list of all publishers"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * \
                    FROM Publisher \
                    ORDER BY name;")
    publishers = cursor.fetchall()

    page = 1  # Because there's a lot of publishers
    max_pages = math.ceil((len(publishers))/ITEMS_PER_PAGE)
    continuing = True
    while continuing is True:
        amounts_min = (page-1)*ITEMS_PER_PAGE
        publisher_list = []
        for i in range(ITEMS_PER_PAGE):  # Just look at these of an amount
            publisher_list.append(publishers[amounts_min])
            amounts_min = amounts_min + 1
        # Print the publishers in a block
        print("-"*36)
        print(f"| {'ID':<5} | Publisher")
        print("-"*36)
        for publisher in publisher_list:
            print(f"| {publisher[0]:<5} | {publisher[1]}")
        print("-"*36)

        # Page switching
        if page == 1:
            while True:
                next = input("Type NEXT for next page, END to retrun to menu: ")
                if next == "NEXT":
                    page = page + 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")
        elif page == max_pages:
            while True:
                next = input("Type BACK for previous page, END to retrun to menu: ")
                if next == "BACK":
                    page = page - 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")
        else:
            while True:
                next = input("Type NEXT for next page, BACK for previous page, END to retrun to menu: ")
                if next == "NEXT":
                    page = page + 1
                    break
                elif next == "BACK":
                    page = page - 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")

    conn.close()  # Close connection to save efficiency


if __name__ == "__main__":
    while True:
        read = input("Id of game: ")
        read_one(read)
        show_genres()
        show_developers()
        show_publishers()
        break
