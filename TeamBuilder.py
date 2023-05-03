import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

conn = sqlite3.connect("../pokemon.sqlite")
c = conn.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Determine it is a number or a string
    try:
        # If it can be converted to an int, assume it is a Pokedex number
        pokedex_number = int(arg)
    except ValueError:
        # Otherwise, assume it is a name and look up the Pokedex number
        c.execute("SELECT pokedex_number FROM pokemon WHERE name = ?", (arg,))
        result = c.fetchone()
        if result is None:
            print("Invalid Pokemon name:", arg)
            sys.exit()
        pokedex_number = result[0]

    # Analyze the Pokemon
    c.execute(
        "SELECT name, type1, type2 FROM pokemon_types_view WHERE name = (SELECT name FROM pokemon WHERE pokedex_number = ?)",
        (pokedex_number,))
    row = c.fetchone()
    if row is not None:
        name, type1, type2 = row
        strong = []
        weak = []
        for t in types:
            against = "against_" + t
            c.execute("SELECT {} FROM pokemon_types_battle_view WHERE type1name = ? AND type2name = ?".format(against),
                      (type1, type2))
            against_val = c.fetchone()[0]
            if against_val > 1:
                strong.append(t)
            elif against_val < 1:
                weak.append(t)
        print("Analyzing", arg)
        print(name, "(" + type1, type2 + ")", "is strong against", strong, "but weak against", weak)
        team.append((name, pokedex_number))


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")