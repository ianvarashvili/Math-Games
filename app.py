# ================================
# app.py
# Flask სერვერის მთავარი ფაილი
# ყველაფერი აქედან იწყება
# ================================

from flask import Flask
from flask_cors import CORS
from firebase_init import db
import os


# Blueprint-ების import
from routes.auth import auth_bp
from routes.game import game_bp
from routes.leaderboard import leaderboard_bp
from routes.progress import progress_bp
from routes.profile import profile_bp

app = Flask(__name__)
CORS(app)

# Blueprint-ების რეგისტრაცია
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(profile_bp)

# ================================
# /health endpoint
# ================================
@app.route("/health")
def health():
    return {"status": "ok", "message": "სერვერი მუშაობს! 🎉"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)