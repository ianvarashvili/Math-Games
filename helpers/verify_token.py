# ================================
# helpers/token_verify.py
# Firebase Token-ის შემოწმება
# ================================

from firebase_admin import auth

def verify_token(auth_header: str) -> str | None:
    """
    Authorization header-იდან Token-ს ამოწმებს.
    ✅ ნამდვილია → აბრუნებს userId-ს
    ❌ არ არის   → აბრუნებს None-ს
    """

    # Header არ არის ან არასწორი ფორმატია?
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    # "Bearer eyJ..." → "eyJ..."
    # .strip() = თეთრ სივრცეებს წაშლის
    token = auth_header.split("Bearer ")[1].strip()

    try:
        decoded = auth.verify_id_token(token)
        # .get() უსაფრთხოა — KeyError-ს არ გამოიტანს
        return decoded.get("uid")

    except auth.ExpiredIdTokenError:
        # Token ვადაგასულია
        return None
    except auth.RevokedIdTokenError:
        # მომხმარებელმა გამოსვლა მოახდინა
        return None
    except auth.InvalidIdTokenError:
        # Token ყალბია
        return None
    except Exception:
        # სხვა მოულოდნელი შეცდომა
        return None
