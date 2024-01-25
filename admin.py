import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("../cs3050-warmup.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {"name": "Los Angeles", "state": "CA", "country": "USA"}

# Add a new doc in collection 'cities' with ID 'LA'
db.collection("cities").document("LA").set(data)