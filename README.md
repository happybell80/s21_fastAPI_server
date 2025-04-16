# Galaxy S21 FastAPI Server

A lightweight FastAPI server implementation designed to run on Samsung Galaxy S21 using Termux.

## Project Overview

This project demonstrates how to use a mobile device (Samsung Galaxy S21) as a web server by:
- Running FastAPI through Termux
- Setting up Nginx as a reverse proxy
- Making the server accessible via the internet using DDNS
- Using modern web technologies (FastAPI, HTMX, TailwindCSS)

## Features

- **Minimal Resource Usage**: Optimized for mobile hardware
- **Modern Tech Stack**: FastAPI backend with HTMX and TailwindCSS frontend
- **External Access**: Accessible from anywhere via DDNS
- **Auto-start**: Configured to start on device boot

## Setup Instructions

1. Install Termux from F-Droid
2. Clone this repository:
   ```bash
   pkg install git
   git clone https://github.com/yourusername/galaxy-s21-fastapi-server.git
   cd galaxy-s21-fastapi-server
   ```

3. Run the setup script:
   ```bash
   chmod +x start_server.sh
   ./start_server.sh
   ```

4. Set up auto-start:
   ```bash
   mkdir -p ~/.termux/boot
   cp startup.sh ~/.termux/boot/
   chmod +x ~/.termux/boot/startup.sh
   ```

5. Install Termux:Boot from F-Droid and grant necessary permissions

## Accessing the Server

- **Local access**: http://localhost:8080
- **External access**: http://rotanevs21.duckdns.org:8080 (replace with your DDNS)
- **API documentation**: http://localhost:8080/docs

## Directory Structure

```
/
├── app.py                 # Main FastAPI application
├── static/                # Static files (CSS, JS, images)
├── templates/             # Jinja2 HTML templates
│   └── index.html         # Main page template
├── nginx.conf             # Nginx configuration
├── start_server.sh        # Manual server starter script
├── startup.sh             # Auto-start script for Termux:Boot
└── README.md              # This file
```

## Development

To develop this application remotely:

1. Connect to the Galaxy S21 via SSH:
   ```bash
   ssh -p 51117 username@rotanevs21.duckdns.org
   ```

2. Use VSCode with Remote SSH extension for easy development

## Future Plans

- [ ] Add HTTPS support
- [ ] Set up AWS EC2 instance as a reverse proxy
- [ ] Implement monitoring and reliability measures
- [ ] Expand API functionality

## License

MIT 