from fastapi import Depends, HTTPException
from typing import Optional

CURRENT_USER = {"username": None, "is_admin": False}

def get_current_user():
    if CURRENT_USER["username"] is None:
        raise HTTPException(status_code=401, detail="Utilisateur non connecté")
    return CURRENT_USER

def admin_required(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Droits admin requis")
    return user
