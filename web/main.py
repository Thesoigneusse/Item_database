from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.database import Database
from models.item import Item

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = Database("dofus.db")

@app.get("/add_item")
async def add_item_form(request: Request):
    return templates.TemplateResponse("add_item.html", {"request": request})

@app.post("/add_item")
async def add_item(
    request: Request,
    name: str = Form(...),
    type: str = Form(...),
    level: int = Form(...),
    main_stats: list[str] = Form([]),
    secondary_stats: list[str] = Form([]),
    damages: list[str] = Form([]),
    resistances: list[str] = Form([])
):
    stats = {
        "main": main_stats,
        "secondary": secondary_stats,
        "damages": damages,
        "resistances": resistances
    }
    item = Item(name=name, type=type, level=level, stats=stats)
    db.add_item(item)
    return RedirectResponse("/add_item", status_code=303)



# # Dossier des templates
# templates = Jinja2Templates(directory="web/templates")

# # Dossier static
# app.mount("/static", StaticFiles(directory="web/static"), name="static")


# @app.get("/")
# def index(request: Request):
#     items = db.get_items()
#     stuffs = db.get_stuffs()
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "items": items,
#         "stuffs": stuffs
#     })


# @app.post("/add_item")
# def add_item(name: str = Form(...), type_: str = Form(...), level: int = Form(...)):
#     # On crée un item vide (stats vides pour le moment)
#     item = Item(name=name, type_=type_, level=level, stats={})
#     db.add_item(item)
#     return RedirectResponse("/", status_code=303)
