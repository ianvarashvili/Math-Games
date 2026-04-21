# ================================
# routes/leaderboard.py
# კლასის რეიტინგი
# ================================

from flask import Blueprint, request, jsonify
from firebase_init import db
from helpers.verify_token import verify_token

leaderboard_bp = Blueprint("leaderboard", __name__)

# ================================
# GET /leaderboard
# კლასის ტოპ 10 + საკუთარი ადგილი
# ================================
@leaderboard_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():

    # ================================
    # 1. Token შემოწმება
    # ================================
    user_id = verify_token(request.headers.get("Authorization"))
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    # ================================
    # 2. grade Firestore-იდან ვიღებთ
    # ფრონტს არ ვენდობით — Token-ით დავადასტურეთ ვინ არის
    # ================================
    user_doc = db.collection("users").document(user_id).get()
    if not user_doc.exists:
        return jsonify({"error": "მომხმარებელი ვერ მოიძებნა"}), 404

    user = user_doc.to_dict()
    grade = user["grade"]

    # ================================
    # 3. იმავე კლასის ყველა მომხმარებელი
    # ================================
    users = db.collection("users")\
              .where("grade", "==", grade)\
              .get()

    # ================================
    # 4. stars-ის მიხედვით დახარისხება
    # ================================
    all_users = []
    for u in users:
        data = u.to_dict()
        all_users.append({
            "userId":   data["userId"],
            "name":     data["name"],
            "avatarId": data["avatarId"],
            "stars":    data["stars"],
            "points":   data["points"] 
        })

    # კლებადობით დალაგება
 
    all_users.sort(key=lambda x: (x["stars"], x["points"]), reverse=True)

    # ================================
    # 5. ადგილების მინიჭება
    # ================================
    for i, u in enumerate(all_users):
        u["place"] = i + 1

    # ================================
    # 6. ტოპ 10
    # ================================
    top10 = all_users[:10]

    # ================================
    # 7. საკუთარი ადგილი
    # ტოპ 10-ში არ იყოს შემთხვევაშიც ჩანს!
    # ================================
    my_place = next(
        (u for u in all_users if u["userId"] == user_id),
        None
    )

    return jsonify({
        "top10":   top10,
        "myPlace": my_place
    }), 200