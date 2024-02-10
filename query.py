import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from admin import connect

# TODO
    # AT THE END ADD IN SUPPORT FOR SOMETHING LIKE avg_rating OF
    # ADD IN genre support for or
    # SPLIT INTO FUNCTIONS

'''
    query is the function to be called by the parser - fetches data from the database based on the query
    param: 
        user_input: a list that contains the query info
    return:
        returns a list of dictionaries with the data requested
'''
def query(user_input):
    db = connect()
    rym_ref = db.collection("rym")
    if user_input[0] != "avg_rating":
        user_input[2] = user_input[2].replace('"', '')
    # assume user input is a list, the first thing is the field we want to search
    # the second thing is the operation, i.e. >, ==, side note, for primary and secondary genres, second input will already be pre determined to be array_contains
    # third is the user input
    # if there is more, then 4 will be AND or OR and 5,6,7 will repeat the first 1,2,3 inputs

    # calls function for and queries
    if "&&" in user_input:
        if user_input[4] != "avg_rating":
            user_input[6] = user_input[6].replace('"', '')
        return and_query(db, rym_ref, user_input)
    
    # calls function for genre queries
    if user_input[0] == "genre":
        return genre_query(db, rym_ref, user_input)
    
    if "||" in user_input:
        if user_input[4] != "avg_rating":
            user_input[6] = user_input[6].replace('"', '')
        return or_query(db, rym_ref, user_input)

    # handles all other queries
    query = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).stream()
    db.close()
    return count_results(query)


''' 
    and_query handles all and queries - helper function for query
    params:
        db: reference to the database so that we can close it in the function
        rym_ref: reference to our actual data
        user_input: a List of strings that we will use to query, has && in it
    return type: 
        list: returns a list of dictionaries of the data that satisfies the users input
'''
def and_query(db, rym_ref, user_input):
    # this is a check for genre, we combined primary and secondary genres together
    if user_input[0] == "genre":
        # array contains is the operator used for arrays in firebase
        user_input[1] = "array_contains"
        # two queries, one to get the && for primary genres and one to get the && for secondary genres
        query_primary = rym_ref.where(filter=FieldFilter("primary_genres", user_input[1], user_input[2])).where(filter=FieldFilter(user_input[4], user_input[5], user_input[6])).stream()
        query_secondary = rym_ref.where(filter=FieldFilter("secondary_genres", user_input[1], user_input[2])).where(filter=FieldFilter(user_input[4], user_input[5], user_input[6])).stream()
        db.close()
        return check_genre_data(query_primary, query_secondary)
    # this code checks the second part of the && for genres
    if user_input[4] == "genre":
        # same comments as above, but we look for genres on the second where now
        user_input[5] = "array_contains"
        query_primary = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).where(filter=FieldFilter("primary_genres", user_input[5], user_input[6])).stream()
        query_secondary = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).where(filter=FieldFilter("secondary_genres", user_input[5], user_input[6])).stream()
        db.close()
        return check_genre_data(query_primary, query_secondary)
    # handles all other && queries besides genre
    query = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).where(filter=FieldFilter(user_input[4], user_input[5], user_input[6])).stream()
    db.close()
    return count_results(query)

'''
    or_query handles all or queries and is a helper function for query()
    params: 
        params:
        db: reference to the database so that we can close it in the function
        rym_ref: reference to our actual data
        user_input: a List of strings that we will use to query, has && in it
    return type: 
        list: returns a list of dictionaries of the data that satisfies the users input
'''
def or_query(db, rym_ref, user_input):
    # this is a check for genre, we combined primary and secondary genres together
    if user_input[0] == "genre":
        #genre_query only expects list of 3 arguments - pass associatred qenre query within or statement
        genre_list = [user_input[0],user_input[1] , user_input[2]]
        genre_result1 = genre_query(db, rym_ref, genre_list)
        # this handles if a user wants to genres
        if user_input[4] == "genre":
            genre_list = [user_input[4],user_input[5] , user_input[6]]
            genre_result2 = genre_query(db, rym_ref, genre_list)
            all_results = genre_result1 + genre_result2
            db.close()
            return remove_dups(all_results)
        #handles second part of or
        query = rym_ref.where(filter=FieldFilter(user_input[4], user_input[5], user_input[6])).stream()
        results1 = count_results(query)
        #put results together
        all_results = genre_result1 + results1
        db.close()
        return remove_dups(all_results)
    # this code checks the second part of the or for genres
    if user_input[4] == "genre":
        # same comments as above, but we look for genres on the second where now
        genre_list = [user_input[4],user_input[5] , user_input[6]]
        genre_result2 = genre_query(db, rym_ref, genre_list)
        query = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).stream()
        results2 = count_results(query)
        all_results = genre_result2 + results2
        db.close()
        return remove_dups(all_results)
    # This code handles all general cases of and besides genres
    filter_1 = FieldFilter(user_input[0], user_input[1], user_input[2])
    filter_2 = FieldFilter(user_input[4], user_input[5], user_input[6])        
    or_filter = Or(filters=[filter_1, filter_2])
    query = rym_ref.where(filter=or_filter).stream()
    db.close()
    return count_results(query)


'''
    remove_dups removes any duplicates in our lists and is a helper function for or_query() which is the only is the only function that can have dups
    params: 
        results: a list of all of our data that will be returned from a query
    returns a list of our data without duplicates
'''
def remove_dups(results):
    for result in results:
            if results.count(result) > 1:
                results.remove(result)
    return results


''' 
    genre_query handles all single genre queries - helper function to query
    params:
        db: reference to the database so that we can close it in the function
        rym_ref: reference to our actual data
        user_input: a List of strings that we will use to query, has && in it
    return type: 
        list: returns a list of dictionaries of the data that satisfies the users input
'''
def genre_query(db, rym_ref, user_input):
    # array_contains is the operator for arrays in firebase
    user_input[1] = "array_contains"
    # query both primary and secondary genres and 
    query_primary = rym_ref.where(filter=FieldFilter("primary_genres", user_input[1], user_input[2])).stream()
    query_secondary = rym_ref.where(filter=FieldFilter("secondary_genres", user_input[1], user_input[2])).stream()
    db.close()
    return check_genre_data(query_primary, query_secondary)

'''
    check_genre_data checks if the query objects returned from queries from genre hold any data 
    if one of the lists contains "No Data" that is removed from the list
    params:
        primary/secondary_query: a query object that holds genre data
    return:
        returns a list of genre data from params
'''
def check_genre_data(primary_query, secondary_query):
    return_primary = count_results(primary_query)
    return_secondary = count_results(secondary_query)
    # if one of the two genres is empty, return the non empty ones
    if return_primary == ["No Data"] and return_secondary != ["No Data"]:
        return return_secondary
    if return_secondary == ["No Data"] and return_primary != ["No Data"]:
        return return_primary
    # return the combination of the primary and secondary genre results
    return_list = return_primary + return_secondary
    return return_list


'''
    count_results takes in a query object and turns them into lists 
    params:
        results: a query object that holds the data that we want to return
    return:
        returns turns the query data into a list of dictionaries, or returns no data if the query object is empty
'''
def count_results(results):
    count = 0
    new_list = []
    for result in results:
        new_list.append(result.to_dict().copy())
        count += 1
    if count == 0:
        return ["No Data"]
    else:
        return new_list

# testing function
def main():
     results = query(["genre", "==", "Art Rock", "&&", "artist_name", "==", "Radiohead"])
     for result in results:
         print(f"{result}")
     return 0
    
# for testing
def print_query(query):
    for result in query:
        print(f"{result}")

def test_or_1():
    results = query(["artist_name", "==", "Bjork", "||", "genre", "==", "Baroque Pop"])
    for result in results:
         print(f"{result}")

def test_or_2():
    results = query(["artist_name", "==", "Bjork", "||", "avg_rating", ">=", 4.3])
    for result in results:
         print(f"{result}")

def test_3():
    results = query(["album_name", "==", "To Pimp a Butterfly"])
    print_query(results)


if __name__ == "__main__":
     #main()
     
     test_3()
    


    