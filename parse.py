from typing import List
import shlex
from query import query

# Class constants

# Positions
QUERY_FIELD_POS = 0
QUERY_OP_POS = 1

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
        user_input = user_input.strip()
        
        #handle commands from user input
        match user_input:
            case "--quit":
                quit = True
            case "--help":
                print_commands()
            case "--example":
                print_example()
            case _:
                try:
                    #split string by spaces
                    #maintain quoted strings as 1 list item
                    input_storage = shlex.split(user_input, posix=False)
                    
                    #validate that query exists
                    if len(input_storage) == 0:
                        print("Invalid - empty query")
                    elif input_storage[0] != "??": 
                        print("Missing ?? at start - please enter a valid query")
                    else:
                        #handle query in depth
                        result = handle_query(input_storage[1:])
                        
                        #if query is valid --> send to query.py
                        if type(result) is list:
                            q = query(result)
                            print_query(q)
                        #if query invalid --> print error message
                        else:
                            print(result)
                #if query would break, print error message
                except ValueError:
                    print("Invalid query - ensure your quotation is correct")
    #end runtime
    print("Exiting")

# Print language description and commands for the user.
def print_commands():
    print("\nWelcome to the album query engine!")
    print(f"Type ?? To start a query. \n"
          f"Then, select a field: artist_name, album_name, avg_rating (0 to 5), genre. \n"
          f"Use standard operators to specify your search: ==, >, <, >=, <=. \n"
          f"Single compound && queries accepted. You cannot search for the same field twice.")
    print("Type --quit to quit, --help to see this message again, or --example to see example valid queries.")
    

# Print example queries for the user.
def print_example():
    print('\n?? artist_name == "Nas"')
    print("?? genre == “Alternative Rock” && avg_rating > 0")


# Handles query input from the user
def handle_query(query: list):
    # Invalid query start cases - returns control to main.

    # Too short query/clause
    if len(query) < 3:
        return "Invalid query - clause too short"

    # Invalid field
    if query[QUERY_FIELD_POS].lower() not in QUERY_VALID_FIELDS:
        return "Invalid field - please enter a valid field"

    # Non-numeric input for avg_rating
    if query[QUERY_FIELD_POS].lower() == "avg_rating":
        try:
            i = float(query[QUERY_OP_POS + 1])
            query[QUERY_OP_POS + 1] = i
        except ValueError:
            return "Invalid data type - must be numeric for avg_rating"

    # Using > < >= <= for string comparison
    if query[QUERY_FIELD_POS].lower() != "avg_rating" and query[QUERY_OP_POS] != "==":
        return "Invalid operator - for string input == is required"

    # Invalid operator
    if query[QUERY_OP_POS] not in QUERY_VALID_OPERATORS:
        return "Unrecognized operator - please enter a valid operator"

    # Query does not begin with a double quote
    if query[QUERY_FIELD_POS].lower() != "avg_rating" and query[QUERY_OP_POS + 1][0] != '"':
        return "Query must begin with a double quote"

    # Handle compound queries - returns a string message if error exists in any clause
    if "&&" in query:
        second_half = query.index("&&") + 1
        compound_query = handle_query(query[second_half:])
        first_half = query[:second_half]
        
        #check that first half of query fits language format
        if len(first_half) != 4:
            return "Invalid query - check quotation and number of inputs"

        #TO DO: add comment
        if type(compound_query) is list:
            first_half.extend(compound_query)
            return first_half
        
        #TO DO: add comment
        else:
            return compound_query
    
    #Handle OR operator    
    elif "||" in query:
        second_half = query.index("||") + 1
        compound_query = handle_query(query[second_half:])
        first_half = query[:second_half]
        
        #TO DO: add comment
        if type(compound_query) is list:
            first_half.extend(compound_query)
            return first_half
        
        #TO DO: add comment
        else:
            return compound_query
    else:
        #check that query fits language format
        if len(query) > 3:
            return "Invalid query - too many inputs"
        else:
            return query
   

#Print dictionary in a readable format
def print_query(query):
    #clead up data returned from Query.py
    for i in query:
        if i == "No Data":
            if len(query) == 1:
                print("No Data")
                return
            else:
                pass
        #Print data
        else:
            print(f"\n{i.get('position')}). Album Name: {i.get('album_name')} By {i.get('artist_name')} with avg rating: {i.get('avg_rating')}")
            print(f"Primary Genres: {i.get('primary_genres')}")
            try:
                print(f"Secondary Genres: {i.get('secondary_genres')}")
                print("--------------------------------------------------------------------------------------------------------------------")
            except:
                print("--------------------------------------------------------------------------------------------------------------------")





# Run main.
if __name__ == "__main__":
    main()