from typing import List

# Class constants

# Positions
QUERY_START_POS = 0
QUERY_FIELD_POS = 1
QUERY_OP_POS = 2
QUERY_DATA_POS = 3

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
                handle_query(input_storage)

           

    print("Exiting")

# Print language description and commands for the user.
def print_commands():
    print("\nWelcome to the album query engine!")
    print(f"Type ?? To start a query. \n"
          f"Then, select a field: artist_name, album_name, avg_rating (0 to 5), genre. \n"
          f"Use standard operators to specify your search: ==, >, <, ≥, ≤. \n"
          f"Single compound && queries accepted.")
    print("Type --quit to quit, --help to see this message again, or --example to see example valid queries.")
    

# Print example queries for the user.
def print_example():
    print('?? artist_name == "Nas"')
    print("?? genre == “Alternative Rock” AND avg_rating > 0")


# Handles query input from the user
def handle_query(query: List[str]):
    # Invalid query start cases - returns control to main.
    if query[QUERY_START_POS] != "??":
        return "Missing ?? at start - please enter a valid query"
    if query[QUERY_FIELD_POS] not in QUERY_VALID_FIELDS:
        return "Invalid field - please enter a valid field"
    if query[QUERY_OP_POS] not in QUERY_VALID_OPERATORS:
        return "Unrecognized operator - please enter a valid operator"

    # Handle multiple word entries - grabs and places into a single string
    full_query_name = ""
    for word in query[QUERY_DATA_POS:]:
        if word == "&&":
            break
        else:
            full_query_name += word

    for i in range(len(query)):
        if query[i] == "AND":
            if query[i+1] not in QUERY_VALID_FIELDS:
                return "Please ender a valid field"

    
    '''else:    
        for i in range(input_storage):
            if input_storage[i] == "==":        
                print(input_storage) '''



# Run main.
if __name__ == "__main__":
    main()