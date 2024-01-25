import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("cs3050-warmup.json")
firebase_admin.initialize_app(cred)

