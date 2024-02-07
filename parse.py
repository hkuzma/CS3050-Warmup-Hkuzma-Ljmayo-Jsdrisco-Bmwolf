from typing import List

# Class constants

# Positions
QUERY_START_POS = 0
QUERY_FIELD_POS = 1
QUERY_OP_POS = 2

# Valid fields & operators
QUERY_VALID_FIELDS = ['artist_name', 'album_name', 'avg_rating', 'genre']
QUERY_VALID_OPERATORS = ['==', '>', '<', '<=', '>=']

# Main loop: grabs user query input and manages help commands.
def main():
    input_storage = []
    quit = False
    print_commands()

    while not quit:
        user_input = input("")
        user_input = user_input.lower().strip()

        match user_input:
            case "--quit":
                quit = True
            case "--help":
                print_commands()
            case "--example":
                print_example()
            case _: 
                input_storage = user_input.split()
                if input_storage[QUERY_START_POS] != "??":
                    print("Please enter a valid query")

    print("Exiting")

# Print language description and commands for the user.
def print_commands():
    print("\nWelcome to the album query engine!")
    print(f"Type ?? To start a query. \n"
          f"Then, select a field: artist_name, album_name, avg_rating (0 to 5), genre. \n"
          f"Use standard operators to specify your search: ==, >, <, >=, <=. \n"
          f"Single compound AND queries accepted.")
    print("Type --quit to quit, --help to see this message again, or --example to see example valid queries.")
    

# Print example queries for the user.
def print_example():
    print('\n ?? artist_name == "Nas"')
    print("?? genre == “Alternative Rock” AND avg_rating > 0")


def handle_query(query: List[str]):
    pass


# Run main.
if __name__ == "__main__":
    main()