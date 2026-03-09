import os
import json
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

@lru_cache(maxsize=1)
def _init_firebase():
    if firebase_admin._apps:
        return

    sa_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

    if sa_json:
        cred = credentials.Certificate(json.loads(sa_json))
    elif sa_path:
        cred = credentials.Certificate(sa_path)
    else:
        raise RuntimeError("Firebase credentials not configured.")

    firebase_admin.initialize_app(cred)

_bearer = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(_bearer)) -> str:
    _init_firebase()
    try:
        decoded = firebase_auth.verify_id_token(token.credentials)
        return decoded["uid"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )
