# ================================
# app.py
# Flask სერვერის მთავარი ფაილი
# ================================

from flask import Flask
from flask_cors import CORS

# firebase_init.py-დან db-ს ვიღებთ
from firebase_init import db

# Flask აპლიკაციის შექმნა
app = Flask(__name__)

# CORS = ფრონტს (სხვა მისამართზე რომ მუშაობს)
# აძლევს ნებას ჩვენს სერვერთან სალაპარაკოდ
CORS(app)

# ================================
# /health endpoint
# ტესტისთვის — სერვერი მუშაობს?
# ბრაუზერში: localhost:5000/health
# ================================
@app.route("/health")
def health():
    return {"status": "ok", "message": "სერვერი მუშაობს! 🎉"}

# სერვერის გაშვება
# debug=True = კოდის შეცვლისას ავტომატურად რესტარტი
# port=5000 = მისამართი იქნება localhost:5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)