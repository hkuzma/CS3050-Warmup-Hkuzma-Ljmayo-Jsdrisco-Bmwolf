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
    
    try:
        df = pd.read_json("CS3050-Warmup-Hkuzma-Ljmayo-Jsdrisco-Bmwolf\\rym.json")
    except Exception:
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
            data = {"position": int(position[i]), "release_name": str(release_name[i]), "artist_name": str(artist_name[i]), 
                    "primary_genres": str(primary_genres[i]), "avg_rating": float(avg_rating[i]), "rating_count": int(rating_count[i])}
        else:
            data = {"position": int(position[i]), "release_name": str(release_name[i]), "artist_name": str(artist_name[i]), 
                    "primary_genres": str(primary_genres[i]), "secondary_genres": str(secondary_genres[i]), "avg_rating": float(avg_rating[i]), "rating_count": int(rating_count[i])}
        db.collection("rym").document(str(position[i])).set(data)
    return 0

if __name__ == "__main__":
    main()