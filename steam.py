import sqlite3
import math

DATABASE_FILE = "steam.db"
ITEMS_PER_PAGE = 40


def display_pages(type, data):
    """Display large amounts of data as pages and switch between"""
    page = 1  # Because there's a lot of data
    max_pages = math.ceil((len(data))/ITEMS_PER_PAGE)
    continuing = True
    while continuing is True:
        amounts_min = (page-1)*ITEMS_PER_PAGE
        my_list = []
        for i in range(ITEMS_PER_PAGE):  # Just look at these of an amount
            my_list.append(data[amounts_min])
            if data[-1] == data[amounts_min]:
                break
            else:
                amounts_min = amounts_min + 1
        # Print the data in a block
        print("-"*36)
        print(f"| {'ID':<7} | {type}")
        print("-"*36)
        for item in my_list:
            print(f"| {item[0]:<7} | {item[1]}")
        print("-"*36)

        # Page switching
        if page == 1 and page == max_pages:  # Only one page
            continuing = False
        elif page == max_pages:  # Last page
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
        elif page == 1:  # First page
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
        else:  # All pages in between
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

    display_pages("Developer", developers)

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

    display_pages("Publisher", publishers)

    conn.close()  # Close connection to save efficiency


def show_in_genre(id):
    """Show list of games within one genre"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT Game.id, \
                           Game.name \
                    FROM Game \
                    JOIN GameGenre ON GameGenre.gameid = Game.id \
                    WHERE GameGenre.genreid = ? \
                    ORDER BY Game.name;", (id,))
    games = cursor.fetchall()
    cursor.execute("SELECT name \
                    FROM Genre \
                    WHERE id = ?", (id,))
    genre = cursor.fetchone()

    print()
    print(f"Games in {genre[0]}")

    # Print list of games in a block as pages
    display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def show_in_dev(id):
    """Show list of games by one developer"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT Game.id, \
                           Game.name \
                    FROM Game \
                    JOIN GameDeveloper ON GameDeveloper.gameid = Game.id \
                    WHERE GameDeveloper.devid = ? \
                    ORDER BY Game.name;", (id,))
    games = cursor.fetchall()
    cursor.execute("SELECT name \
                    FROM Developer \
                    WHERE id = ?", (id,))
    developer = cursor.fetchone()

    print()
    print(f"Games by {developer[0]}")

    # Print list of games in a block as pages
    display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def show_in_publisher(id):
    """Show list of games by one publisher"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT Game.id, \
                           Game.name \
                    FROM Game \
                    JOIN GamePublisher ON GamePublisher.gameid = Game.id \
                    WHERE GamePublisher.publishid = ? \
                    ORDER BY Game.name;", (id,))
    games = cursor.fetchall()
    cursor.execute("SELECT name \
                    FROM Publisher \
                    WHERE id = ?", (id,))
    publisher = cursor.fetchone()

    print()
    print(f"Games by {publisher[0]}")

    # Print list of games in a block as pages
    display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def search_game_by_name():
    """Search game by name rather than id, shows list of all possibilities"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    search = input("Search games by name: ")
    search = f"%{search}%"
    cursor.execute("SELECT id, \
                           name \
                    FROM Game \
                    WHERE name LIKE ?;", (search,))
    games = cursor.fetchall()

    display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def search_dev_by_name():
    """Search developer by name rather than id, shows list of all possibilities"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    search = input("Search developers by name: ")
    search = f"%{search}%"
    cursor.execute("SELECT id, \
                           name \
                    FROM Developer \
                    WHERE name LIKE ?;", (search,))
    devs = cursor.fetchall()

    display_pages("Developer", devs)

    conn.close()  # Close connection to save efficiency


def search_publisher_by_name():
    """Search publisher by name rather than id, shows list of all possibilities"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    search = input("Search publishers by name: ")
    search = f"%{search}%"
    cursor.execute("SELECT id, \
                           name \
                    FROM Publisher \
                    WHERE name LIKE ?;", (search,))
    publishers = cursor.fetchall()

    display_pages("Publisher", publishers)

    conn.close()  # Close connection to save efficiency


if __name__ == "__main__":
    while True:
        # read = input("Id of game: ")
        # read_one(read)
        # show_genres()
        # show_developers()
        # show_publishers()
        # genre_id = int(input("Id of genre: "))
        # show_in_genre(genre_id)
        # dev_id = int(input("Id of developer: "))
        # show_in_dev(dev_id)
        # publisher_id = int(input("Id of publisher: "))
        # show_in_publisher(publisher_id)
        # search_game_by_name()
        # search_dev_by_name()
        search_publisher_by_name()
        break
