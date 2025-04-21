from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import logging

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
        {"request": request, "title": "Goose Farm Investing - Every tokenized real-world asset, in one place."}
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """
    Serve the about page
    """
    return templates.TemplateResponse(
        "about.html", 
        {"request": request, "title": "About - "}
    )

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    """
    Serve the blog page
    """
    return templates.TemplateResponse(
        "blog.html", 
        {"request": request, "title": "Research Blog - Goose Farm Investing"}
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
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting server in development mode with auto-reload enabled")
    
    # Run the server if executed as script
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        reload_dirs=["./"],
        log_level="info"
    ) 