import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials






# Use a service account.
cred = credentials.Certificate('FireStorePrivateKey\epiuse-bd49f-f86c050ead9b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def CheckIfIDInDatabase(ID):

    #Create reference employees_ref for 'Employees' collection in Firestore database
    employees_ref = db.collection("Employees").stream()

    employees = []

    #Concert every document in collection to dictionary and append to employees list
    for emp in employees_ref:
        employees.append(emp.to_dict())

    for emp in employees:
        if str(emp['ID']) == str(ID):
            return True
    
    return False