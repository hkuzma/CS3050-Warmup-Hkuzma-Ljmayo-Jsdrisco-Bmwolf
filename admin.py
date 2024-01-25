import firebase_admin
from firebase_admin import firestore
import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("cs3050-warmup.json")
firebase_admin.initialize_app(cred)

db = firestore.client()