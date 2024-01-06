import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

def call(p_id):
    # Use a service account
    cred = credentials.Certificate('./mykey.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection('IV').document(p_id)
    output = users_ref.get().to_dict()['remain']

    print(output)

call(sys.argv[1])
