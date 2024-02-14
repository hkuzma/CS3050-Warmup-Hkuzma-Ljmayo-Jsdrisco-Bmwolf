import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import pandas as pd
import sys

# connect function
# returns a reference to the db
def connect():
    # checks to see if a db connection is already initialized, if its not, initialize one
    if not firebase_admin._apps:
        cred = credentials.Certificate("../cs3050-warmup.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def main():
    db = connect()
    
    # check to see if they add only 1 additional argument to run
    if len(sys.argv) != 2:
        print("Please enter the name of a json file")
        return 1

    # try to read the json, if not return
    try:
        df = pd.read_json(sys.argv[1])
    except:
        print("Error reading json file")
        return 1

    # parse everything
    position = df["position"].values
    release_name = df["release_name"].values
    artist_name = df["artist_name"].values
    primary_genres = df["primary_genres"].values
    secondary_genres = df["secondary_genres"].values
    avg_rating = df["avg_rating"].values
    rating_count = df["rating_count"].values
    
    # go through the data
    for i in range(0, len(position)):
        # if there isnt a secondary genre, dont add that to the data base
        if pd.isna(secondary_genres[i]):
            # turn primary genres into a list
            primary_genres[i] = str(primary_genres[i])
            genreList = primary_genres[i].split(", ")
            # data to be sent
            data = {"position": int(position[i]), "album_name": str(release_name[i]), "artist_name": str(artist_name[i]), 
                    "primary_genres": genreList, "avg_rating": float(avg_rating[i]), "rating_count": int(rating_count[i])}
        else:
            # turn primary and secondary genres into lists
            primary_genres[i] = str(primary_genres[i])
            primaryGenreList = primary_genres[i].split(", ")
            secondary_genres[i] = str(secondary_genres[i])
            secondaryGenresList = secondary_genres[i].split(", ")
            data = {"position": int(position[i]), "album_name": str(release_name[i]), "artist_name": str(artist_name[i]), 
                    "primary_genres": primaryGenreList, "secondary_genres": secondaryGenresList, "avg_rating": float(avg_rating[i]), "rating_count": int(rating_count[i])}
        # send the data
        db.collection("rym").document(str(position[i])).set(data)
    # close the database
    print("Updated db")
    db.close()
    return 0

if __name__ == "__main__":
    main()