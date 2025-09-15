from typing import List
from fastapi import FastAPI, Request, Form, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from db.database import Database
from models.item import Item
import json

from Utils import STATS_CATEGORIES

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

db = Database()

# ---------------------------
# Gestion utilisateurs simples
# ---------------------------
with open("users.json", "r") as f:
    USERS = json.load(f)

# Utilisateur connecté simulé
CURRENT_USER = {"username": None, "is_admin": False}

def get_current_user():
    return CURRENT_USER

def admin_required(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Droits admin requis")
    return user

# ---------------------------
# Routes login / logout
# ---------------------------
@app.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    global CURRENT_USER
    user = next((u for u in USERS if u["username"] == username and u["password"] == password), None)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Identifiants invalides"})
    CURRENT_USER = {"username": user["username"], "is_admin": user["is_admin"]}
    return RedirectResponse("/", status_code=303)

@app.get("/logout")
async def logout():
    global CURRENT_USER
    CURRENT_USER = {"username": None, "is_admin": False}
    return RedirectResponse("/", status_code=303)


# --- Page principale ---
@app.get("/")
async def index(request: Request):
    user_items = db.get_items(perfect=False)   # [(id, Item), ...]
    perfect_items = db.get_items(perfect=True) # [(id, Item), ...]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_items": user_items,
            "perfect_items": perfect_items,
            "current_user": CURRENT_USER
        }
    )

### Ajout ###
# --- Ajouter un item personnalisé ---
@app.get("/add_user_item")
async def add_user_item_form(request: Request):
    return templates.TemplateResponse("add_user_item.html", {"request": request, "current_user": CURRENT_USER})

@app.post("/add_user_item")
async def add_user_item(
    request: Request,
    name: str = Form(...),
    categorie: str = Form(...),
    level: int = Form(...),
    stats: str = Form(...)
    ):
    form_data = await request.form()
    stats_dict = {}
    for category, stats_list in STATS_CATEGORIES.items():
        for stat in stats_list:
            key = f"stat_{stat.replace(' ', '_')}"
            value = form_data.get(key)
            stats_dict[stat] = int(value) if value and value.strip() != "" else None

    item = Item(name=name, categorie=categorie, level=level, stats=stats_dict)
    db.add_item(item, perfect=False)
    return RedirectResponse("/", status_code=303)

# --- Ajouter un item parfait ---
@app.get("/add_perfect_item")
async def add_perfect_item_form(request: Request, user=Depends(admin_required)):
    return templates.TemplateResponse("add_perfect_item.html", {
        "request": request,
        "categories": STATS_CATEGORIES,
        "current_user": CURRENT_USER
    })

@app.post("/add_perfect_item")
async def add_perfect_item(request: Request, user=Depends(admin_required),
                           name: str = Form(...),
                           categorie: str = Form(...),
                           level: int = Form(...)):
    form_data = await request.form()
    stats = {}
    for category, stats_list in STATS_CATEGORIES.items():
        for stat in stats_list:
            key = f"stat_{stat.replace(' ', '_')}"
            value = form_data.get(key)
            stats[stat] = int(value) if value and value.strip() != "" else None

    item = Item(name=name, categorie=categorie, level=level, stats=stats)
    db.add_item(item, perfect=True)
    return RedirectResponse("/", status_code=303)

# --- Modifier un item utilisateur ou parfait et le copier dans la DB utilisateur ---
@app.get("/edit_user_or_perfect_item/{item_id}/{source}")
async def edit_user_or_perfect_item_form(request: Request, item_id: int, source: str):
    items = db.get_items(perfect=(source=="perfect"))
    item_tuple = next((i for i in items if i[0] == item_id), None)
    if item_tuple is None:
        return RedirectResponse("/", status_code=303)

    item_id, item = item_tuple
    return templates.TemplateResponse("edit_user_or_perfect_item.html", {
        "request": request,
        "item_id": item_id,
        "item": item,
        "source": source,
        "categories": STATS_CATEGORIES,
        "current_user": CURRENT_USER
    })

@app.post("/edit_user_or_perfect_item/{item_id}/{source}")
async def edit_user_or_perfect_item(
    request: Request,
    item_id: int,
    source: str,
    name: str = Form(...),
    categorie: str = Form(...),
    level: int = Form(...),
    copy: bool = Form(False)
):
    form_data = await request.form()
    stats_dict = {}
    for category, stats_list in STATS_CATEGORIES.items():
        for stat in stats_list:
            key = f"stat_{stat.replace(' ', '_')}"
            value = form_data.get(key)
            stats_dict[stat] = int(value) if value and value.strip() != "" else None

    item = Item(name=name, categorie=categorie, level=level, stats=stats_dict)

    if source == "perfect":
        # Tout item parfait modifié devient un nouvel item utilisateur
        db.add_item(item, perfect=False)
    else:
        if copy:
            db.add_item(item, perfect=False)
        else:
            db.update_item(item_id, item, perfect=False)

    return RedirectResponse("/", status_code=303)

# --- Supprimer un item utilisateur ou parfait ---
@app.get("/delete_item/{item_id}/{source}")
async def delete_item(item_id: int, source: str, user=Depends(get_current_user)):
    """
    Supprime un item de la base de données.
    
    source: "user" ou "perfect"
    L'utilisateur doit être connecté. Pour supprimer un item parfait, il doit être admin.
    """
    if source == "perfect":
        # Admin uniquement
        db.delete_item(item_id, perfect=True, force=True)
    else:
        # Tous les utilisateurs connectés peuvent supprimer leurs items
        db.delete_item(item_id, perfect=False)
    
    return RedirectResponse("/", status_code=303)



