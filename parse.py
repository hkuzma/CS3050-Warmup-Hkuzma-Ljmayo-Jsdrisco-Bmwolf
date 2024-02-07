def main():
    quit = False
    while quit != True:
        user_input = input("??\n")
        user_input = user_input.lower()
        if user_input == "quit":
            quit = True
            break
        if user_input == "help":
            printCommands()
    print("Exiting")





def printCommands():
    print("Welcome to the album query engine!")
    print(f"Type ?? To start a query. \n"
          f"Then, select a field: artist_name, album_name, avg_rating (0 to 5), genre. \n"
          f"Use standard operators to specify your search: ==, >, <, ≥, ≤. \n")
    print("Type --quit to quit, --help to see this message again, or --example to see example valid queries.")
    
    
def printExample():
    print("?? genre == “Alternative Rock” AND avg_rating > 0")

if __name__ == "__main__":
    main()