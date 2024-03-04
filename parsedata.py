import csv

with open("steam.csv", "r", encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile)
    for game in csvreader:
        if game[0] == "279580":
            print(game)
