# ================================
# routes/game.py
# თამაშის შედეგის მიღება და დამუშავება
# ================================

from flask import Blueprint, request, jsonify
from firebase_init import db
from helpers.verify_token import verify_token
from helpers.rank import calculate_rank
from helpers.badges import check_badges
import uuid
from datetime import datetime

game_bp = Blueprint("game", __name__)

# ================================
# POST /game/submit
# თამაშის შედეგის გაგზავნა
# ================================
@game_bp.route("/game/submit", methods=["POST"])
def submit_game():
    data = request.get_json()

    # ================================
    # 1. Token-ის შემოწმება
    # ================================
    user_id = verify_token(request.headers.get("Authorization"))
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401

    # ================================
    # 2. ველების შემოწმება
    # ================================
    required = [
        "userId", "gameId", "island", "gameGrade",
        "actionsTotal", "actionsCorrect",
        "timeSpentSeconds", "maxTimeSeconds"
    ]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} აკლია"}), 400

    # Token-ის userId და გაგზავნილი userId ემთხვევა?
    # ბავშვი სხვის სახელით ვერ გაგზავნის!
    if user_id != data["userId"]:
        return jsonify({"error": "unauthorized"}), 401

    actions_total   = data["actionsTotal"]
    actions_correct = data["actionsCorrect"]
    time_spent      = data["timeSpentSeconds"]
    max_time        = data["maxTimeSeconds"]
    game_grade      = data["gameGrade"]
    island          = data["island"]
    game_id         = data["gameId"]

    # ================================
    # 3. ქულების გამოთვლა
    # ================================

    # edge case: ბავშვი შევიდა და გავიდა — 0 მოქმედება
    if actions_total == 0:
        accuracy_score = 0
        speed_score    = 0
        total_score    = 0
        stars          = 0
        counted        = False
    else:
        # სიზუსტე: სწორი/სულ * 50
        accuracy_score = round((actions_correct / actions_total) * 50)

        # სიჩქარე: დარჩენილი დრო / მაქსიმუმი * 50
        speed_score = max(0, round(
            ((max_time - time_spent) / max_time) * 50
        ))

        # სულ ქულა
        total_score = accuracy_score + speed_score

        # ვარსკვლავები
        if total_score >= 80:
            stars = 3
        elif total_score >= 50:
            stars = 2
        else:
            stars = 1

        # ითვლება რანკინგში?
        # მხოლოდ თავის კლასში თამაშისას
        user_doc = db.collection("users").document(user_id).get()
        user     = user_doc.to_dict()
        counted  = user["grade"] == game_grade

    # ================================
    # 4. /scores-ში შენახვა
    # ================================
    score_id = str(uuid.uuid4())
    db.collection("scores").document(score_id).set({
        "scoreId":        score_id,
        "userId":         user_id,
        "gameId":         game_id,
        "island":         island,
        "gameGrade":      game_grade,
        "actionsTotal":   actions_total,
        "actionsCorrect": actions_correct,
        "accuracyScore":  accuracy_score,
        "speedScore":     speed_score,
        "totalScore":     total_score,
        "stars":          stars,
        "timeSpentSeconds": time_spent,
        "countedForRanking": counted,
        "createdAt":      datetime.utcnow()
    })

    # ================================
    # 5. /users განახლება
    # მხოლოდ countedForRanking == True შემთხვევაში
    # ================================
    new_badges    = []
    updated_stars  = user["stars"]
    updated_points = user["points"]
    updated_rank   = user["rank"]

    if counted:
        updated_stars  = user["stars"] + stars
        updated_points = user["points"] + total_score
        updated_rank   = calculate_rank(updated_points)

        # ბეიჯების შემოწმება
        all_scores = db.collection("scores")\
                       .where("userId", "==", user_id)\
                       .get()
        all_scores_list = [s.to_dict() for s in all_scores]

        new_badges = check_badges(
            user["badges"],
            all_scores_list,
            data
        )

        updated_badges = user["badges"] + new_badges

        # Firestore განახლება
        db.collection("users").document(user_id).update({
            "stars":  updated_stars,
            "points": updated_points,
            "rank":   updated_rank,
            "badges": updated_badges
        })

    # ================================
    # 6. ფრონტს ვაბრუნებთ
    # ================================
    return jsonify({
        "totalScore":    total_score,
        "stars":         stars,
        "newBadges":     new_badges,
        "updatedStars":  updated_stars,
        "updatedPoints": updated_points,
        "updatedRank":   updated_rank
    }), 200