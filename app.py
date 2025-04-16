from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

# Create FastAPI app instance
app = FastAPI(title="Galaxy S21 FastAPI Server", 
              description="A FastAPI server running on Samsung Galaxy S21 via Termux")

# Create directory for templates and static files if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve the home page
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Galaxy S21 FastAPI Server"}
    )

@app.get("/api/status")
async def status():
    """
    Simple API endpoint to check server status
    """
    return {
        "status": "online",
        "server": "Galaxy S21 with Termux",
        "framework": "FastAPI"
    }

# Add more API endpoints as needed

if __name__ == "__main__":
    # Run the server if executed as script
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True) 