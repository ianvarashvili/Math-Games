# ================================
# routes/progress.py
# კუნძულების პროგრესი და გახსნის სტატუსი
# ================================

from flask import Blueprint, request, jsonify
from firebase_init import db
from helpers.verify_token import verify_token

progress_bp = Blueprint("progress", __name__)

# ================================
# GET /progress
# კუნძულების სტატუსი
# ================================
@progress_bp.route("/progress", methods=["GET"])
def get_progress():

    # ================================
    # 1. Token შემოწმება
    # ================================
    user_id = verify_token(request.headers.get("Authorization"))
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    # ================================
    # 2. User Firestore-იდან
    # grade გვჭირდება — ფრონტს არ ვენდობით
    # ================================
    user_doc = db.collection("users").document(user_id).get()
    if not user_doc.exists:
        return jsonify({"error": "მომხმარებელი ვერ მოიძებნა"}), 404

    user = user_doc.to_dict()
    grade = user["grade"]

    # ================================
    # 3. User-ის scores Firestore-იდან
    # მხოლოდ countedForRanking==True — თავის კლასი!
    # სხვა კლასში თამაში პროგრესში არ ითვლება
    # ================================
    scores = db.collection("scores")\
               .where("userId", "==", user_id)\
               .where("countedForRanking", "==", True)\
               .get()

    scores_list = [s.to_dict() for s in scores]

    # ================================
    # 4. თითო კუნძულზე completedGames
    # ================================
    def count_island(island_name):
        """
        კონკრეტული კუნძულის დასრულებული თამაშების რაოდენობა.
        იგივე gameId ორჯერ რომ ითამაშა — ერთხელ ვითვლით!
        """
        # unique gameId-ები ამ კუნძულზე
        unique_games = set(
            s["gameId"] for s in scores_list
            if s.get("island") == island_name
        )
        return len(unique_games)

    castle_count    = count_island("castle")
    jungle_count    = count_island("jungle")
    labyrinth_count = count_island("labyrinth")

    # ================================
    # 5. კუნძულების გახსნის პირობები
    # ================================

    # castle → ყოველთვის unlocked
    castle_unlocked = True

    # jungle → castle-ზე >= 3 უნიკალური თამაში
    jungle_unlocked = castle_count >= 3

    # labyrinth → jungle-ზე >= 3 უნიკალური თამაში
    labyrinth_unlocked = jungle_count >= 3

    # ================================
    # 6. ფრონტს ვაბრუნებთ
    # ================================
    return jsonify({
        "castle": {
            "unlocked":      castle_unlocked,
            "completedGames": castle_count
        },
        "jungle": {
            "unlocked":      jungle_unlocked,
            "completedGames": jungle_count
        },
        "labyrinth": {
            "unlocked":      labyrinth_unlocked,
            "completedGames": labyrinth_count
        }
    }), 200