# ================================
# app.py
# Flask სერვერის მთავარი ფაილი
# ყველაფერი აქედან იწყება
# ================================

from flask import Flask
from flask_cors import CORS
from firebase_init import db

# Blueprint-ების import
# თითო route ფაილიდან Blueprint-ს ვიღებთ
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

# Blueprint-ების რეგისტრაცია
# ახლა /auth/register და /auth/login ხელმისაწვდომია
app.register_blueprint(auth_bp)

# ================================
# /health endpoint
# ================================
@app.route("/health")
def health():
    return {"status": "ok", "message": "სერვერი მუშაობს! 🎉"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)