# ================================
# test_firebase.py
# Firebase კავშირის ტესტი
# შემდეგ წავშლით!
# ================================

from firebase_init import db

# ტესტური მონაცემის ჩაწერა
db.collection("test").document("hello").set({
    "message": "Firebase მუშაობს! 🎉"
})

# ჩაწერილის წაკითხვა
doc = db.collection("test").document("hello").get()
print(doc.to_dict())