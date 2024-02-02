import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from admin import connect


def parser(user_input):
    db = connect()
    rym_ref = db.collection("rym")
    # assume user input is a list, the first thing is the field we want to search
    # the second thing is the operation, i.e. >, ==, side note, for primary and secondary genres, second input will already be pre determined to be array-contains
    # third is the user input
    # if there is more, then 4 will be AND or OR and 5,6,7 will repeat the first 1,2,3 inputs
    if "AND" in user_input:
        query = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).where(filter=FieldFilter(user_input[4], user_input[5], user_input[6])).stream()
        db.close()
        return count_results(query)
    if "OR" in user_input:
        filter_1 = FieldFilter(user_input[0], user_input[1], user_input[2])
        filter_2 = FieldFilter(user_input[4], user_input[5], user_input[6])
        or_filter = Or(filters=[filter_1, filter_2])
        query = rym_ref.where(filter=or_filter).stream()
        db.close()
        return count_results(query)
    if user_input[0] == "primary_genres" or "secondary_genres":
        query = rym_ref.where(filter=FieldFilter(user_input[0], "array-contains", user_input[2])).stream()
        db.close()
        return count_results(query)
    query = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).stream()
    db.close()
    return count_results(query)

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

# def main():
#     results = parser(["avg_rating", ">", 4.2, "OR", "artist_name", "==", "Radiohead"])
#     for result in results:
#         print(f"{result}")
#     return 0

# if __name__ == "__main__":
#     main()