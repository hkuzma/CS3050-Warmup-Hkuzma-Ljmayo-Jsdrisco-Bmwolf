import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def connect():
    cred = credentials.Certificate("../cs3050-warmup.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def main():
    return 0

if __name__ == "__main__":
    main()