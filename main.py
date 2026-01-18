from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import ai, downloader, maker, search, random
import uvicorn
import os

app = FastAPI(
    title="Kagenta API",
    description="The Ultimate Nexus of Intelligence and Tools",
    version="3.0.0",
    docs_url="/docs",
    redoc_url=None
)

# Register All Routers
app.include_router(ai.router)
app.include_router(downloader.router)
app.include_router(maker.router)
app.include_router(search.router)
app.include_router(random.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Read the HTML template
    file_path = os.path.join(os.path.dirname(__file__), "app/templates/index.html")
    with open(file_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)