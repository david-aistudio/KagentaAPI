from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routers import ai, downloader, maker, search, random, islamic, information, game
import uvicorn
import os

# Disable default Swagger/ReDoc
app = FastAPI(
    title="Kagenta API",
    description="The Ultimate Nexus of Intelligence and Tools",
    version="3.0.0",
    docs_url=None, # SWAGGER KILLED
    redoc_url=None # REDOC KILLED
)

# Register All Routers
app.include_router(ai.router)
app.include_router(downloader.router)
app.include_router(maker.router)
app.include_router(search.router)
app.include_router(random.router)
app.include_router(islamic.router)
app.include_router(information.router)
app.include_router(game.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Read the HTML template
    file_path = os.path.join(os.path.dirname(__file__), "app/templates/index.html")
    with open(file_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
