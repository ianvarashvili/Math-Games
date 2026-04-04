# ================================
# helpers/badges.py
# ბეიჯების შემოწმება და დარიცხვა
# ================================
# გამოყენება:
# from helpers.badges import check_badges
# ================================


def check_badges(
    current_badges: list[str],
    all_scores: list[dict],
    current_score: dict
) -> list[str]:
    """
    ბეიჯების პირობებს ამოწმებს და ახლა დამსახურებულ ბეიჯებს აბრუნებს.

    Args:
        current_badges (list[str]):
            ბეიჯები, რომლებიც მომხმარებელს უკვე აქვს.
        all_scores (list[dict]):
            მომხმარებლის ყველა თამაშის შედეგი Firestore-იდან.
        current_score (dict):
            ახლახან დასრულებული თამაშის რეკორდი (არ არის მონაწილეობის
            პირობა, მხოლოდ ლოგიკური მითითება).

    Returns:
        list[str]: ახალი ბეიჯების სია, რომლებიც ამ მომენტში დაიმსახურა.
    """
    new_badges = []


    # ================================
    # 🏅 სწრაფი მოაზროვნე
    # პირობა: 5 თამაშში speedScore == 50
    # ================================
    if "სწრაფი მოაზროვნე" not in current_badges:
        max_speed_count = sum(
            1 for s in all_scores
            if s.get("speedScore") is not None and s["speedScore"] == 50
        )
        if max_speed_count >= 5:
            new_badges.append("სწრაფი მოაზროვნე")


    # ================================
    # 🏅 უშეცდომო
    # პირობა: ერთ კუნძულზე ყველა თამაში accuracyScore == 50
    # ================================
    if "უშეცდომო" not in current_badges:
        islands = ["castle", "jungle", "labyrinth"]

        for island in islands:
            island_scores = [
                s for s in all_scores
                if s.get("island") == island
            ]
            # კუნძულზე 5 თამაში უნდა იყოს და ყველას სრულყოფილი სიზუსტე
            if len(island_scores) >= 5 and all(
                s.get("accuracyScore") is not None and s["accuracyScore"] == 50
                for s in island_scores
            ):
                new_badges.append("უშეცდომო")
                break  # როდესაც ერთი კუნძული აკმაყოფილებს, აღარ ვამოწმებთ დანარჩენებს


    # ================================
    # 🏅 გამრავლების ოსტატი
    # პირობა: castle კუნძული III კლასში ⭐⭐⭐ (stars == 3)
    # ================================
    if "გამრავლების ოსტატი" not in current_badges:
        castle_grade3 = [
            s for s in all_scores
            if s.get("island") == "castle"
            and s.get("gameGrade") == 3
            and s.get("stars") == 3
        ]
        # 5 თამაში ყველა 3 ვარსკვლავით
        if len(castle_grade3) >= 5:
            new_badges.append("გამრავლების ოსტატი")


    return new_badges