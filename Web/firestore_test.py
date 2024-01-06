import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

def call():
    # Use a service account
    cred = credentials.Certificate('./mykey.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection('IV')
    output = users_ref.stream()
    
    for doc in output:
        print(u'{}'.format(doc.to_dict()))

    # print(output)

call()
