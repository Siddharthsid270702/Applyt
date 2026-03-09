import os
import json
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

# ---------------------------------------------------------------------------
# Firebase Admin initialisation
# ---------------------------------------------------------------------------
# Option A: Set FIREBASE_SERVICE_ACCOUNT_JSON to the full JSON string (Render secret)
# Option B: Set FIREBASE_SERVICE_ACCOUNT_PATH to the path of the JSON file
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _init_firebase():
    if firebase_admin._apps:
        return  # already initialised

    sa_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

    if sa_json:
        sa_dict = json.loads(sa_json)
        cred = credentials.Certificate(sa_dict)
    elif sa_path:
        cred = credentials.Certificate(sa_path)
    else:
        raise RuntimeError(
            "Firebase credentials not configured. "
            "Set FIREBASE_SERVICE_ACCOUNT_JSON or FIREBASE_SERVICE_ACCOUNT_PATH."
        )

    firebase_admin.initialize_app(cred)


_bearer = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    """
    Verify the Firebase ID token sent in the Authorization header.
    Returns the uid (user_id string) on success.
    """
    _init_firebase()
    try:
        decoded = firebase_auth.verify_id_token(token.credentials)
        return decoded["uid"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )
