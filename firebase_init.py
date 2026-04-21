# ================================
# firebase_init.py
# Firebase-თან კავშირის ფაილი
# ================================

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# ლოკალურად → serviceAccountKey.json
# Render.com-ზე → Environment Variable
if os.path.exists("serviceAccountKey.json"):
    cred = credentials.Certificate("serviceAccountKey.json")
else:
    service_account = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT"))
    cred = credentials.Certificate(service_account)

firebase_admin.initialize_app(cred)
db = firestore.client()