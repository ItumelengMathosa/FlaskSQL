import hashlib

from InitializeFirestore import *

#Get all documents from Users collection
user_ref = db.collection("users").stream()

USERS = []

#Append all documents as dictionaries to USERS list
for doc in user_ref:
    USERS.append(doc.to_dict())


def Hash(value):
    #Use sha256 hashing library
    hasher = hashlib.sha256()
    hasher.update(value.encode('utf-8'))
    hashedvalue = hasher.hexdigest()

    return hashedvalue

def ValidateUser(username, password, users=USERS):
    
    verdict = None

    hashedpassword = Hash(password)

    for user in users:
        if user['Username'] == username:
            if user['Password'] == hashedpassword:
                verdict = True
                return verdict
            else:
                verdict = "Incorrect password"
                return verdict
        else:
            verdict = "Username not found"

    return verdict

def UpdateUserPasswordInDatabase(username, newPassword):
    doc_ref = db.collection("Users").document(str(username))
    doc_ref.update({"Password":newPassword})
    return