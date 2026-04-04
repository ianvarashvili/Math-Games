# ================================
# routes/auth.py
# რეგისტრაცია და შესვლა
# ================================

from flask import Blueprint, request, jsonify
from firebase_admin import auth
from firebase_init import db
import bcrypt
import requests as req
import os
from dotenv import load_dotenv

# .env ფაილიდან ცვლადების ჩატვირთვა
load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Blueprint = route-ების "ჯგუფი"
# app.py-ში ამ ჯგუფს მთლიანად დავარეგისტრირებთ
auth_bp = Blueprint("auth", __name__)

# ================================
# POST /auth/register
# ახალი მომხმარებლის რეგისტრაცია
# ================================
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    # ფრონტიდან მოსული მონაცემები
    data = request.get_json()

    # ველების არსებობის შემოწმება
    required = ["username", "password", "name", "surname", "avatarId", "grade"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} აკლია"}), 400

    username = data["username"].strip().lower()
    password = data["password"]
    name     = data["name"].strip()
    surname  = data["surname"].strip()
    avatar_id = data["avatarId"]
    grade    = data["grade"]

    # grade შემოწმება — მხოლოდ 1,2,3,4
    if grade not in [1, 2, 3, 4]:
        return jsonify({"error": "კლასი უნდა იყოს 1-4"}), 400

    # username უნიკალურია?
    existing = db.collection("users")\
                 .where("username", "==", username)\
                 .get()
    if len(existing) > 0:
        return jsonify({"error": "username უკვე არსებობს"}), 409

    # password-ის hash-ვა
    # bcrypt.hashpw = password → დაშიფრული სტრიქონი
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Firebase Auth-ში მომხმარებლის შექმნა
    # email-ად username@mathgame.ge ვიყენებთ
    try:
        firebase_user = auth.create_user(
            email=f"{username}@mathgame.ge",
            password=password
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Firestore-ში მომხმარებლის შენახვა
    db.collection("users").document(firebase_user.uid).set({
        "userId":   firebase_user.uid,
        "username": username,
        "password": hashed_password,
        "name":     name,
        "surname":  surname,
        "avatarId": avatar_id,
        "grade":    grade,
        "stars":    0,
        "points":   0,
        "rank":     "მათემატიკის მოსწავლე",
        "badges":   [],
        "createdAt": __import__("datetime").datetime.utcnow()
    })

    return jsonify({"success": True, "userId": firebase_user.uid}), 201

  # ================================
# POST /auth/login
# მომხმარებლის შესვლა
# ================================
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    # ველების შემოწმება
    if "username" not in data or "password" not in data:
        return jsonify({"error": "username და password აუცილებელია"}), 400

    username = data["username"].strip().lower()
    password = data["password"]

    # Firestore-იდან username-ით ვეძებთ
    users = db.collection("users")\
              .where("username", "==", username)\
              .get()

    if len(users) == 0:
        return jsonify({"error": "მომხმარებელი ვერ მოიძებნა"}), 404

    user = users[0].to_dict()

    # password-ის შემოწმება
    password_correct = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    if not password_correct:
        return jsonify({"error": "პაროლი არასწორია"}), 401

    # Firebase REST API-ით idToken-ს ვიღებთ
    # idToken = ჩვენი verify_token-ისთვის საჭირო token
    try:
        
       
        
        response = req.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
            json={
                "email": f"{username}@mathgame.ge",
                "password": password,
                "returnSecureToken": True
            }
        )
        token_data = response.json()
        id_token = token_data["idToken"]

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "firebaseToken": id_token,
        "userId":        user["userId"],
        "name":          user["name"],
        "surname":       user["surname"],
        "avatarId":      user["avatarId"],
        "grade":         user["grade"],
        "stars":         user["stars"],
        "points":        user["points"],
        "rank":          user["rank"],
        "badges":        user["badges"]
    }), 200