# ================================
# firebase_init.py
# Firebase-თან კავშირის ფაილი
# ================================
# ეს ფაილი სხვა ფაილებში ასე გამოიყენება:
# from firebase_init import db
# ================================

import firebase_admin
from firebase_admin import credentials, firestore

# credentials = "ვინ ვარ მე?" → Firebase-ს ვეუბნებით
# serviceAccountKey.json = ჩვენი პირადობის მოწმობა
cred = credentials.Certificate("serviceAccountKey.json")

# Firebase-ის ინიციალიზაცია — ერთხელ ხდება
firebase_admin.initialize_app(cred)

# db = მონაცემთა ბაზის ობიექტი
# სხვა ფაილები ამ db-ს გამოიყენებენ
# მაგ: db.collection("users").document("123").get()
db = firestore.client()