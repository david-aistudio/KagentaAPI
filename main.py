from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routers import mail
import uvicorn
import os

# Disable default Swagger/ReDoc
app = FastAPI(
    title="KagentaMail",
    description="Premium Disposable Email Service",
    version="1.3.0-LITE",
    docs_url=None, 
    redoc_url=None
)

# Register Routers
app.include_router(mail.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    file_path = os.path.join(os.path.dirname(__file__), "app/templates/index.html")
    with open(file_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
