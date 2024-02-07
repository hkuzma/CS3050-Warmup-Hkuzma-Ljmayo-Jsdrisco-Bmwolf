from typing import List
import shlex

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
                input_storage = shlex.split(user_input, posix=False)
                result = handle_query(input_storage)
                print(result)

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
    print("?? genre == “Alternative Rock” && avg_rating > 0")


# Handles query input from the user
def handle_query(query: List[str]):
    # Invalid query start cases - returns control to main.
    if len(query) == 0:
        return "Invalid query"
    if query[QUERY_START_POS] != "??":
        return "Missing ?? at start - please enter a valid query"
    if query[QUERY_FIELD_POS] not in QUERY_VALID_FIELDS:
        return "Invalid field - please enter a valid field"
    if query[QUERY_OP_POS] not in QUERY_VALID_OPERATORS:
        return "Unrecognized operator - please enter a valid operator"

    query_list = query
    # Handle multiple word entries - grabs and places into a single string
    compound_query = None
    if "&&" in query:
        second_half = query.index("&&") + 1
        compound_query = handle_query(query[second_half:])
        if compound_query is type(list):
            query_list.extend(compound_query)
        else:
            return compound_query
    
    '''else:    
        for i in range(input_storage):
            if input_storage[i] == "==":        
                print(input_storage) '''



# Run main.
if __name__ == "__main__":
    main()