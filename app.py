from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import os
import logging
import secrets
import base64

# Create FastAPI app instance
app = FastAPI(title="Galaxy S21 FastAPI Server", 
            description="A FastAPI server running on Samsung Galaxy S21 via Termux")

# Content Security Policy middleware
class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 각 요청마다 고유한 nonce 생성
        nonce = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
        
        # 요청 객체에 nonce 저장
        request.state.csp_nonce = nonce
        
        response = await call_next(request)
        
        # 기본 CSP 적용 (nonce 포함)
        csp_header = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://cdnjs.cloudflare.com; "
            f"style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            f"img-src 'self' data:; "
            f"font-src 'self' https://cdnjs.cloudflare.com; "
            f"connect-src 'self'; "
            f"media-src 'self'; "
            f"object-src 'none'; "
            f"frame-src 'self'; "
            f"base-uri 'self'; "
            f"form-action 'self';"
        )
        
        response.headers["Content-Security-Policy"] = csp_header
        return response

# Add CSP middleware
app.add_middleware(CSPMiddleware)

# Create directory for templates and static files if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/img", exist_ok=True)
os.makedirs("templates/ko", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve the English home page
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """
    Serve the about page
    """
    return templates.TemplateResponse(
        "about.html", 
        {"request": request, "title": "About - GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
    )

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    """
    Serve the blog page
    """
    return templates.TemplateResponse(
        "blog.html", 
        {"request": request, "title": "Research Blog - GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
    )

@app.get("/ko/", response_class=HTMLResponse)
async def korean_root(request: Request):
    """
    Serve the Korean home page
    """
    return templates.TemplateResponse(
        "ko/index.html", 
        {"request": request, "title": "GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
    )

@app.get("/ko/about", response_class=HTMLResponse)
async def korean_about(request: Request):
    """
    Serve the Korean about page
    """
    return templates.TemplateResponse(
        "ko/about.html", 
        {"request": request, "title": "소개 - GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
    )

@app.get("/ko/blog", response_class=HTMLResponse)
async def korean_blog(request: Request):
    """
    Serve the Korean blog page
    """
    return templates.TemplateResponse(
        "ko/blog.html", 
        {"request": request, "title": "리서치 블로그 - GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
    )

@app.get("/ko/{path:path}", response_class=HTMLResponse)
async def korean_pages(request: Request, path: str):
    """
    Handle Korean language routes
    Try to serve the appropriate Korean template
    Fall back to English if not available
    """
    # Check if the Korean template exists
    ko_template = f"ko/{path}.html"
    if os.path.exists(f"templates/{ko_template}"):
        return templates.TemplateResponse(
            ko_template,
            {"request": request, "title": "GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
        )
    
    # If Korean template doesn't exist, check if English exists
    en_template = f"{path}.html"
    if os.path.exists(f"templates/{en_template}"):
        # Redirect to English version
        return RedirectResponse(url=f"/{path}")
    
    # If neither exists, redirect to Korean home
    return RedirectResponse(url="/ko/")

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