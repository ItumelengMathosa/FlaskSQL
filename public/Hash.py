import hashlib

from InitializeFirestore import *

def generate_gravatar_url(email, size=200, default_image=None):
    # Calculate the MD5 hash of the email
    md5_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    # Build the Gravatar URL
    gravatar_url = f"https://www.gravatar.com/avatar/{md5_hash}?s={size}"
    if default_image:
        gravatar_url += f"&d={default_image}"

    return gravatar_url

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