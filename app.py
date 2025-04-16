from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
import uvicorn
import os
import psutil
import time
import platform
import json
from datetime import datetime
from typing import Dict, List, Any

# Create FastAPI app instance
app = FastAPI(title="Galaxy S21 FastAPI Server", 
            description="A FastAPI server running on Samsung Galaxy S21 via Termux")

# Create directory for templates and static files if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Store monitoring data
MAX_DATA_POINTS = 60  # Store last 60 data points (10 minutes at 10s intervals)
monitoring_data = {
    "cpu": [],
    "memory": [],
    "disk": [],
    "network": [],
    "timestamps": []
}

# Clear old monitoring data file on start
monitoring_file = "data/monitoring_data.json"
if os.path.exists(monitoring_file):
    with open(monitoring_file, "w") as f:
        json.dump(monitoring_data, f)

@app.on_event("startup")
@repeat_every(seconds=10)  # Update every 10 seconds
async def collect_system_stats():
    """Collect system statistics periodically"""
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # Network stats (just count, not actual bandwidth)
        network_stats = psutil.net_io_counters()
        network_sent = network_stats.bytes_sent
        network_recv = network_stats.bytes_recv
        
        # Store data with timestamps
        if len(monitoring_data["timestamps"]) >= MAX_DATA_POINTS:
            monitoring_data["timestamps"].pop(0)
            monitoring_data["cpu"].pop(0)
            monitoring_data["memory"].pop(0)
            monitoring_data["disk"].pop(0)
            monitoring_data["network"].pop(0)
            
        monitoring_data["timestamps"].append(timestamp)
        monitoring_data["cpu"].append(cpu_percent)
        monitoring_data["memory"].append(memory_percent)
        monitoring_data["disk"].append(disk_percent)
        monitoring_data["network"].append({
            "sent": network_sent,
            "received": network_recv
        })
        
        # Save to file (for persistence)
        with open(monitoring_file, "w") as f:
            json.dump(monitoring_data, f)
            
    except Exception as e:
        print(f"Error collecting system stats: {e}")

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

@app.get("/monitoring", response_class=HTMLResponse)
async def monitoring_dashboard(request: Request):
    """
    Server monitoring dashboard
    """
    uptime = time.time() - psutil.boot_time()
    days, remainder = divmod(uptime, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    # System info
    system_info = {
        "hostname": platform.node(),
        "platform": platform.system(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "uptime": uptime_str
    }
    
    return templates.TemplateResponse(
        "monitoring.html", 
        {
            "request": request,
            "title": "System Monitoring", 
            "system_info": system_info
        }
    )

@app.get("/api/monitoring/current")
async def current_monitoring_data():
    """
    API endpoint for current system monitoring data
    """
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 * 1024)  # Convert to MB
        memory_total = memory.total / (1024 * 1024)  # Convert to MB
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_used = disk.used / (1024 * 1024 * 1024)  # Convert to GB
        disk_total = disk.total / (1024 * 1024 * 1024)  # Convert to GB
        disk_percent = disk.percent
        
        # Process count
        process_count = len(psutil.pids())
        
        # Temperature (may not work on all devices)
        temp_info = {}
        try:
            temp_info = psutil.sensors_temperatures()
        except:
            pass
        
        # Battery info (may not work on all devices)
        battery_info = {}
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_info = {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "secsleft": battery.secsleft
                }
        except:
            pass
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": cpu_percent
            },
            "memory": {
                "used": round(memory_used, 2),
                "total": round(memory_total, 2),
                "percent": memory_percent
            },
            "disk": {
                "used": round(disk_used, 2),
                "total": round(disk_total, 2),
                "percent": disk_percent
            },
            "process_count": process_count,
            "temperature": temp_info,
            "battery": battery_info
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/monitoring/history")
async def monitoring_history():
    """
    API endpoint for historical monitoring data
    """
    return monitoring_data

# Add more API endpoints as needed

if __name__ == "__main__":
    # Run the server if executed as script
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True) 