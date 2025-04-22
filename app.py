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
from datetime import datetime, timedelta
import random

# Create FastAPI app instance
app = FastAPI(title="Galaxy S21 FastAPI Server", 
            description="A FastAPI server running on Samsung Galaxy S21 via Termux")

# Create directory for templates and static files if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/img", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("templates/ko", exist_ok=True)
os.makedirs("templates/ko/includes", exist_ok=True)
os.makedirs("templates/includes", exist_ok=True)

# Mount static files directory - 중요: CSP 미들웨어 등록 전에 위치
app.mount("/static", StaticFiles(directory="static"), name="static")

# Content Security Policy middleware
class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 정적 파일 요청인 경우 즉시 처리
        if request.url.path.startswith("/static"):
            return await call_next(request)
            
        # 각 요청마다 고유한 nonce 생성
        nonce = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
        
        # 요청 객체에 nonce 저장
        request.state.csp_nonce = nonce
        
        response = await call_next(request)
        
        # 기본 CSP 적용 (nonce 포함)
        csp_header = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' 'unsafe-eval' https://cdnjs.cloudflare.com https://d3js.org; "
            f"style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            f"img-src 'self' data: https:; "
            f"font-src 'self' https://cdnjs.cloudflare.com https://fonts.gstatic.com; "
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

@app.get("/analysis", response_class=HTMLResponse)
async def analysis(request: Request):
    """
    Serve the analysis page with global market overview
    """
    return templates.TemplateResponse(
        "analysis.html", 
        {"request": request, "title": "Market Analysis - GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
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

@app.get("/ko/analysis", response_class=HTMLResponse)
async def korean_analysis(request: Request):
    """
    Serve the Korean analysis page with global market overview
    """
    return templates.TemplateResponse(
        "ko/analysis.html", 
        {"request": request, "title": "시장 분석 - GooseFarmInvesting.com", "csp_nonce": request.state.csp_nonce}
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

@app.get("/api/rwa/overview")
async def get_rwa_overview():
    """
    API endpoint to provide RWA overview metrics
    """
    return {
        "totalRwa": "$21.19B",
        "assetHolders": 97619,
        "assetIssuers": 185,
        "stablecoinValue": "$227.23B",
        "stablecoinHolders": 158880000,
        "change30d": "+9.78%"
    }

@app.get("/api/rwa/series")
async def get_rwa_series():
    """
    API endpoint to provide time series data for RWA charts
    """
    return {
        "dates": ["2023-01-01", "2023-04-01", "2023-07-01", "2023-10-01", "2024-01-01", "2024-04-01"],
        "values": [5e9, 8e9, 12e9, 15e9, 18e9, 21.19e9],
        "marketShare": {
            "labels": ["Ethereum", "ZKsync Era", "Stellar", "Aptos", "Algorand", "Others"],
            "values": [56.03, 20.71, 4.45, 3.12, 3.09, 12.6]
        }
    }

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

@app.get("/api/analytics/metrics")
async def metrics():
    """
    API endpoint to provide analytics metrics
    """
    return {
        "totalUsers": {"value": "32,456", "change": 12.3},
        "activeTraders": {"value": "8,754", "change": 5.7},
        "tradingVolume": {"value": "$24.5M", "change": -3.2},
        "marketCap": {"value": "$158.7B", "change": 7.8}
    }

@app.get("/api/analytics/charts")
async def charts():
    """
    API endpoint to provide chart data
    """
    # Market trends data
    today = datetime.now()
    market_trends = []
    for i in range(30, -1, -1):
        date = today - timedelta(days=i)
        market_trends.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": 10000 + random.random() * 5000
        })
    
    # Token distribution data
    token_distribution = [
        {"category": "BTC", "value": 45},
        {"category": "ETH", "value": 30},
        {"category": "XRP", "value": 10},
        {"category": "SOL", "value": 8},
        {"category": "Others", "value": 7}
    ]
    
    # Trading volume data
    trading_volume = []
    for i in range(12):
        date = today.replace(month=((today.month - 11 + i) % 12) or 12, 
                             year=today.year + ((today.month - 11 + i) // 12))
        trading_volume.append({
            "date": date.strftime("%Y-%m"),
            "value": 5000000 + random.random() * 10000000
        })
    
    # Price comparison data
    price_comparison = []
    for i in range(30, -1, -1):
        date = today - timedelta(days=i)
        price_comparison.append({
            "date": date.strftime("%Y-%m-%d"),
            "BTC": 30000 + random.random() * 5000,
            "ETH": 2000 + random.random() * 500,
            "XRP": 0.5 + random.random() * 0.2,
            "SOL": 100 + random.random() * 20
        })
    
    return {
        "marketTrends": market_trends,
        "tokenDistribution": token_distribution,
        "tradingVolume": trading_volume,
        "priceComparison": price_comparison
    }

@app.get("/api/analytics/transactions")
async def transactions():
    """
    API endpoint to provide transaction data
    """
    transactions = []
    types = ["Buy", "Sell", "Transfer", "Swap"]
    tokens = ["BTC", "ETH", "XRP", "SOL", "USDT"]
    statuses = ["Completed", "Pending", "Failed"]
    
    for i in range(1, 21):
        today = datetime.now()
        random_days = random.randint(0, 30)
        date = today - timedelta(days=random_days)
        
        transactions.append({
            "id": f"TX{100000 + i}",
            "type": random.choice(types),
            "amount": round(random.random() * 10, 4),
            "token": random.choice(tokens),
            "status": random.choice(statuses),
            "date": date.strftime("%Y-%m-%d")
        })
    
    return transactions

@app.get("/api/analytics/news")
async def news():
    """
    API endpoint to provide news data
    """
    return [
        {
            "title": "Bitcoin Surges Past $50K as Institutional Adoption Grows",
            "summary": "Bitcoin has surpassed the $50,000 mark for the first time in months as institutional investors continue to show interest in cryptocurrency.",
            "source": "CryptoNews",
            "date": "2023-10-15",
            "url": "#"
        },
        {
            "title": "New Regulatory Framework for Crypto Exchanges Announced",
            "summary": "The Securities and Exchange Commission has announced a new regulatory framework that aims to provide clarity for cryptocurrency exchanges.",
            "source": "Financial Times",
            "date": "2023-10-12",
            "url": "#"
        },
        {
            "title": "Ethereum 2.0 Upgrade Set to Launch Next Month",
            "summary": "The much-anticipated Ethereum 2.0 upgrade is scheduled to launch next month, promising improved scalability and reduced energy consumption.",
            "source": "Tech Insider",
            "date": "2023-10-10",
            "url": "#"
        },
        {
            "title": "DeFi Market Cap Reaches All-Time High of $150 Billion",
            "summary": "The total market capitalization of decentralized finance (DeFi) projects has reached an all-time high of $150 billion, reflecting growing investor confidence.",
            "source": "DeFi Pulse",
            "date": "2023-10-08",
            "url": "#"
        }
    ]

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