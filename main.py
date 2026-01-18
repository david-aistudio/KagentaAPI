from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routers import native, z_router
import uvicorn
import os

# Disable default Swagger/ReDoc
app = FastAPI(
    title="Kagenta API",
    description="The Native AI Engine",
    version="4.0.0-NATIVE",
    docs_url=None, # SWAGGER KILLED
    redoc_url=None # REDOC KILLED
)

# Register Routers
app.include_router(native.router)
app.include_router(z_router.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    # Read the HTML template
    file_path = os.path.join(os.path.dirname(__file__), "app/templates/index.html")
    with open(file_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
