# Main loop: grabs user query input and manages help commands.
def main():
    quit = False
    printCommands()

    while not quit:
        user_input = input("")
        user_input = user_input.lower().strip()

        match user_input:
            case "--quit":
                quit = True
            case "--help":
                printCommands()

    print("Exiting")

def printCommands():
    print("\nWelcome to the album query engine!")
    print(f"Type ?? To start a query. \n"
          f"Then, select a field: artist_name, album_name, avg_rating (0 to 5), genre. \n"
          f"Use standard operators to specify your search: ==, >, <, ≥, ≤. \n")
    print("Type --quit to quit, --help to see this message again, or --example to see example valid queries.")
    
    
def printExample():
    print("?? genre == “Alternative Rock” AND avg_rating > 0")

if __name__ == "__main__":
    main()