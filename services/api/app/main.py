# Boardy — сервис уведомлений и ленты (Python/FastAPI).
import time
import threading
import os
import pymysql
import redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.database import get_db

app = FastAPI(title="Boardy Notifications", root_path="/api")


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: str):
        for ws in list(self.active):
            await ws.send_text(message)


manager = ConnectionManager()


def poll_ads():
    r = redis.Redis(host="redis", port=6379)
    last_seen = None
    while True:
        try:
            msg = r.get("last_ad")
            if msg and msg != last_seen:
                last_seen = msg
                print("DEBUG got ad:", msg)
        except:
            pass
        time.sleep(2)


@app.on_event("startup")
def startup():
    threading.Thread(target=poll_ads, daemon=True).start()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/feed")
def feed():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id, title, price FROM ads ORDER BY id DESC LIMIT 20")
        rows = cur.fetchall()
    db.close()
    print("DEBUG feed size:", len(rows))
    return {"items": rows}


@app.get("/health")
def health():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id FROM ads")
    db.close()
    return {"status": "ok"}

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
