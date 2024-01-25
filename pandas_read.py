import numpy as np
import pandas as pd
import sys

df = pd.read_json("CS3050-Warmup-Hkuzma-Ljmayo-Jsdrisco-Bmwolf\\rym.json")

position = df["position"].values
release_name = df["release_name"].values
artist_name = df["release_name"].values
primary_genres = df["primary_genres"].values
secondary_genres = df["secondary_genres"].values
avg_rating = df["avg_rating"].values
rating_count = df["rating_count"].values

