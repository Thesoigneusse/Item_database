from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from dependencies import CURRENT_USER

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

with open("users.json", "r") as f:
    USERS = json.load(f)

@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = next((u for u in USERS if u["username"] == username and u["password"] == password), None)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Identifiants invalides"})
    CURRENT_USER.update({"username": user["username"], "is_admin": user["is_admin"]})
    return RedirectResponse("/", status_code=303)

@router.get("/logout")
async def logout():
    CURRENT_USER.update({"username": None, "is_admin": False})
    return RedirectResponse("/", status_code=303)
