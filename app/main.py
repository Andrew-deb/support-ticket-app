from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.routes import tickets, messages

app = FastAPI(
    title="Support Ticket App",
    description="Internal support ticket system backed by Lakebase",
    version="1.0.0",
)

# Register route handlers
app.include_router(tickets.router)
app.include_router(messages.router)

# Serve static frontend files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def serve_homepage():
    """Serve the main HTML page."""
    return FileResponse(static_dir / "index.html")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("DATABRICKS_APP_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

