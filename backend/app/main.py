import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .database.connection import engine
from .database.database import Base
from . import models  # noqa: F401 - registers SQLAlchemy models
from .routes import auth, cargo, personnel, inventory, location, checkin, alerts, emergency, expedition, dashboard


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message: str):
        dead = []
        for connection in self.connections:
            try:
                await connection.send_text(message)
            except Exception:
                dead.append(connection)
        for connection in dead:
            self.disconnect(connection)


manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates missing tables for the prototype. Existing tables are not dropped.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Integrated Polar Expedition Logistics and Asset Management System",
    description="SIH backend for expedition planning, cargo tracking, inventory, personnel movement and emergency response.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [auth.router, expedition.router, personnel.router, cargo.router, inventory.router, location.router, checkin.router, alerts.router, emergency.router, dashboard.router]:
    app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "project": "Integrated Polar Expedition Logistics and Asset Management System",
        "service": "Expedition Control Center API",
        "status": "running",
        "docs": "/docs",
    }

@app.get("/api/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "OK", "database": "Connected", "timestamp": datetime.now(timezone.utc)}

@app.websocket("/ws/live")
async def live_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
