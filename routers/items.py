from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from dependencies import get_current_user, admin_required
from db.database import Database
from models.item import Item
from Utils.STATS_CATEGORIES import STATS_CATEGORIES

router = APIRouter()
db = Database()
templates = Jinja2Templates(directory="web/templates")

### Ajout ###
# --- Ajouter un item personnalisé ---
@router.get("/add_user_item")
async def add_user_item_form(request: Request, CURRENT_USER=Depends(get_current_user)):
    return templates.TemplateResponse("add_user_item.html", {
        "request": request,
        "categories": STATS_CATEGORIES,
        "current_user": CURRENT_USER})

@router.post("/add_user_item")
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
@router.get("/add_perfect_item")
async def add_perfect_item_form(request: Request, CURRENT_USER=Depends(get_current_user)):
    return templates.TemplateResponse("add_perfect_item.html", {
        "request": request,
        "categories": STATS_CATEGORIES,
        "current_user": CURRENT_USER
    })

@router.post("/add_perfect_item")
async def add_perfect_item(request: Request, 
                           CURRENT_USER=Depends(get_current_user),
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

# --- Modifier un item parfait et le copier modifié dans la DB utilisateur ---
@router.get("/edit_perfect_item_to_user_db/{item_id}")
async def edit_perfect_item_to_user_db_form(request: Request, item_id: int, CURRENT_USER=Depends(get_current_user)):
    # Récupérer l'item parfait correspondant
    perfect_items = db.get_items(perfect=True)
    item_tuple = next((i for i in perfect_items if i[0] == item_id), None)
    if item_tuple is None:
        return RedirectResponse("/", status_code=303)

    _, item = item_tuple
    return templates.TemplateResponse("edit_perfect_item_to_user_db.html", {
        "request": request,
        "item_id": item_id,
        "item": item,
        "source": "perfect",
        "categories": STATS_CATEGORIES,
        "current_user": CURRENT_USER
    })

@router.post("/edit_perfect_item_to_user_db/{item_id}")
async def edit_perfect_item_to_user_db(
    request: Request,
    item_id: int,
    name: str = Form(...),
    categorie: str = Form(...),
    level: int = Form(...),
    CURRENT_USER=Depends(get_current_user)
):
    form_data = await request.form()

    # Construire le dict des stats à partir du formulaire
    stats_dict = {}
    for category, stats_list in STATS_CATEGORIES.items():
        for stat in stats_list:
            key = f"stat_{stat.replace(' ', '_')}"
            value = form_data.get(key)
            stats_dict[stat] = int(value) if value and value.strip() != "" else None

    # Créer un nouvel item utilisateur
    item = Item(name=name, categorie=categorie, level=level, stats=stats_dict)
    db.add_item(item, perfect=False)

    return RedirectResponse("/", status_code=303)


# --- Supprimer un item utilisateur ou parfait ---
@router.get("/delete_perfect_item/{item_id}")
async def delete_perfect_item(item_id: int, user=Depends(get_current_user)):
    """
    Supprime un item de la base de données.
    
    L'utilisateur doit être connecté. Pour supprimer un item parfait, il doit être admin.
    """
    # Admin uniquement
    db.delete_item(item_id, perfect=True, force=True)
    
    return RedirectResponse("/", status_code=303)

# --- Supprimer un item utilisateur ou parfait ---
@router.get("/delete_user_item/{item_id}")
async def delete_user_item(item_id: int, user=Depends(get_current_user)):
    """
    Supprime un item de la base de données.
    
    L'utilisateur doit être connecté.
    """
    # Admin uniquement
    db.delete_item(item_id, perfect=False, force=False)
    
    return RedirectResponse("/", status_code=303)


