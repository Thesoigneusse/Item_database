from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request
from dependencies import get_current_user
from fastapi.responses import RedirectResponse

from routers import items
from auth import router as auth_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")

templates = Jinja2Templates(directory="web/templates")

app.include_router(auth_router)
app.include_router(items.router)

@app.get("/")
async def index(request: Request):
    try:
        user = get_current_user()
    except:
        return RedirectResponse("/login", status_code=303)

    from db.database import Database
    db = Database()
    user_items = db.get_items(perfect=False)
    perfect_items = db.get_items(perfect=True)

    return templates.TemplateResponse("index.html", {
        "request": request,  # <-- ici
        "user_items": user_items,
        "perfect_items": perfect_items,
        "current_user": user
    })