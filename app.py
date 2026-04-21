# ================================
# app.py
# Flask სერვერის მთავარი ფაილი
# ყველაფერი აქედან იწყება
# ================================

from flask import Flask
from flask_cors import CORS
from firebase_init import db


# Blueprint-ების import
from routes.auth import auth_bp
from routes.game import game_bp
from routes.leaderboard import leaderboard_bp
from routes.progress import progress_bp

app = Flask(__name__)
CORS(app)

# Blueprint-ების რეგისტრაცია
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(progress_bp)

# ================================
# /health endpoint
# ================================
@app.route("/health")
def health():
    return {"status": "ok", "message": "სერვერი მუშაობს! 🎉"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)