import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials






# Use a service account.
cred = credentials.Certificate('FireStorePrivateKey\epiuse-bd49f-f86c050ead9b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def CheckIfValueInDatabase(value):

    #Create reference employees_ref for 'Employees' collection in Firestore database
    employees_ref = db.collection("Employees").stream()

    data = []

    #Convert every document in collection to dictionary and append to data list
    for document in employees_ref:
        data.append(document.to_dict())

    #Iterate through all dictionaries in 'data'list and return true if value is in one of the dictionaries
    for dictionary in data:
        if value in dictionary.values():
            return True
    
    return False