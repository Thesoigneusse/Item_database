from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.database import Database
from models.item import Item

app = FastAPI()
db = Database("dofus.db")

# Dossier des templates
templates = Jinja2Templates(directory="templates")

# Dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index(request: Request):
    items = db.get_items()
    stuffs = db.get_stuffs()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "items": items,
        "stuffs": stuffs
    })


@app.post("/add_item")
def add_item(name: str = Form(...), type_: str = Form(...), level: int = Form(...)):
    # On crée un item vide (stats vides pour le moment)
    item = Item(name=name, type_=type_, level=level, stats={})
    db.add_item(item)
    return RedirectResponse("/", status_code=303)
