import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import album
import numpy as np
import pandas as pd

def connect():
    cred = credentials.Certificate("../cs3050-warmup.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def main():
    db = connect()
    
    df = pd.read_json("rym.json")

    position = df["position"].values
    release_name = df["release_name"].values
    artist_name = df["artist_name"].values
    primary_genres = df["primary_genres"].values
    secondary_genres = df["secondary_genres"].values
    avg_rating = df["avg_rating"].values
    rating_count = df["rating_count"].values
    
    for i in range(0, len(position)):
        if pd.isna(secondary_genres[i]):
            primary_genres[i] = str(primary_genres[i])
            genreList = primary_genres[i].split(", ")
            data = {"position": int(position[i]), "album_name": str(release_name[i]), "artist_name": str(artist_name[i]), 
                    "primary_genres": genreList, "avg_rating": float(avg_rating[i]), "rating_count": int(rating_count[i])}
        else:
            primary_genres[i] = str(primary_genres[i])
            primaryGenreList = primary_genres[i].split(", ")
            secondary_genres[i] = str(secondary_genres[i])
            secondaryGenresList = secondary_genres[i].split(", ")
            data = {"position": int(position[i]), "album_name": str(release_name[i]), "artist_name": str(artist_name[i]), 
                    "primary_genres": primaryGenreList, "secondary_genres": secondaryGenresList, "avg_rating": float(avg_rating[i]), "rating_count": int(rating_count[i])}
        db.collection("rym").document(str(position[i])).set(data)
    return 0

if __name__ == "__main__":
    main()