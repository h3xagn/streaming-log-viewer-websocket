"""
FastAPI Streaming Log Viewer over WebSockets

1. Read last n-lines from specified log file
2. Stream log data over WebSockets
3. Simple log viewer page
"""

# import libraries
from pathlib import Path
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio

# set path and log file name
base_dir = Path(__file__).resolve().parent
log_file = "app.log"

# create fastapi instance
app = FastAPI()

# set template and static file directories for Jinja
templates = Jinja2Templates(directory=str(Path(base_dir, "templates")))
app.mount("/static", StaticFiles(directory="static"), name="static")

async def log_reader(n=5) -> list:
    """Log reader

    Args:
        n (int, optional): number of lines to read from file. Defaults to 5.

    Returns:
        list: List containing last n-lines in log file with html tags.
    """
    log_lines = []
    with open(f"{base_dir}/{log_file}", "r") as file:
        for line in file.readlines()[-n:]:
            if line.__contains__("ERROR"):
                log_lines.append(f'<span class="text-red-400">{line}</span><br/>')
            elif line.__contains__("WARNING"):
                log_lines.append(f'<span class="text-orange-300">{line}</span><br/>')
            else:
                log_lines.append(f"{line}<br/>")
        return log_lines


@app.get("/")
async def get(request: Request) -> templates.TemplateResponse:
    """Log file viewer

    Args:
        request (Request): Default web request.

    Returns:
        TemplateResponse: Jinja template with context data.
    """
    context = {"title": "FastAPI Streaming Log Viewer over WebSockets", "log_file": log_file}
    return templates.TemplateResponse("index.html", {"request": request, "context": context})


@app.websocket("/ws/log")
async def websocket_endpoint_log(websocket: WebSocket) -> None:
    """WebSocket endpoint for client connections

    Args:
        websocket (WebSocket): WebSocket request from client.
    """
    await websocket.accept()

    try:
        while True:
            await asyncio.sleep(1)
            logs = await log_reader(30)
            await websocket.send_text(logs)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()

# set parameters to run uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True,
        workers=1,
        debug=True,
    )
