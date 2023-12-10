import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials




# Use a service account.
cred = credentials.Certificate('FireStorePrivateKey\epiuse-bd49f-f86c050ead9b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()



