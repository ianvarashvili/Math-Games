# ================================
# routes/profile.py
# პროფილის განახლება
# ================================

from flask import Blueprint, request, jsonify
from firebase_init import db
from helpers.verify_token import verify_token

profile_bp = Blueprint("profile", __name__)

# ================================
# PATCH /profile/update
# ავატარის, სახელის, გვარის განახლება
# ================================
@profile_bp.route("/profile/update", methods=["PATCH"])
def update_profile():

    data = request.get_json()

    # ================================
    # 1. Token შემოწმება
    # ================================
    user_id = verify_token(request.headers.get("Authorization"))
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    # ================================
    # 2. userId შემოწმება
    # Token-ის userId == გაგზავნილი userId?
    # სხვის პროფილს ვერ შეცვლის!
    # ================================
    if "userId" not in data:
        return jsonify({"error": "userId აკლია"}), 400

    if user_id != data["userId"]:
        return jsonify({"error": "unauthorized"}), 401

    # ================================
    # 3. რა იცვლება?
    # ყველაფერი optional — მხოლოდ გაგზავნილი ველები განახლდება
    # ================================
    updates = {}

    if "avatarId" in data:
        updates["avatarId"] = data["avatarId"]

    if "name" in data:
        name = data["name"].strip()
        if not name:
            return jsonify({"error": "სახელი ცარიელია"}), 400
        updates["name"] = name

    if "surname" in data:
        surname = data["surname"].strip()
        if not surname:
            return jsonify({"error": "გვარი ცარიელია"}), 400
        updates["surname"] = surname

    # არაფერი გამოგზავნილა?
    if not updates:
        return jsonify({"error": "განსახლებელი ველი არ არის"}), 400

    # ================================
    # 4. Firestore განახლება
    # ================================
    db.collection("users").document(user_id).update(updates)

    return jsonify({"success": True}), 200