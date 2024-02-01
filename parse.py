import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from admin import connect


def parser(user_input):
    db = connect()
    rym_ref = db.collection("rym")
    if user_input[0] == "primary_genres" or "secondary_genres":
        query = rym_ref.where(filter=FieldFilter(user_input[0], user_input[1], user_input[2])).stream()
        print("Returned Query")
        return query
    print("Exiting parser")
    db.close()

def main():
    results = parser(["primary_genres", "array_contains", "Art Rock"])
    print("hello")
    for result in results:
        print(f"{result.id} => {result.to_dict()}")

if __name__ == "__main__":
    main()