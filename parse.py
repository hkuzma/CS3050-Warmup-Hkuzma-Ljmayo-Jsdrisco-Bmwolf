# Main loop: grabs user query input and manages help commands.
def main():
    input_storage = []
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
            case _: 
                input_storage = user_input.split()
                if(input_storage[] != "??"):
                    print("Please enter a valid query")
                if(input_storage[])
                
                else:    
                    for i in range(input_storage):
                        if input_storage[i] == "==":
                        
                         print(input_storage)

    print("Exiting")

def printCommands():
    print("\nWelcome to the album query engine!")
    print(f"Type ?? To start a query. \n"
          f"Then, select a field: artist_name, album_name, avg_rating (0 to 5), genre. \n"
          f"Use standard operators to specify your search: ==, >, <, ≥, ≤. \n"
          f"Single compound AND queries accepted.")
    print("Type --quit to quit, --help to see this message again, or --example to see example valid queries.")
    
    
def printExample():
    print("?? genre == “Alternative Rock” AND avg_rating > 0")

if __name__ == "__main__":
    main()