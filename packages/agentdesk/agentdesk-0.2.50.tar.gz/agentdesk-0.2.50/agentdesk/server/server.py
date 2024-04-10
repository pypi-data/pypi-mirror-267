from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import V1Desktop, V1Desktops, V1DesktopReqeust, V1DesktopRegistration
from agentdesk.vm import DesktopVM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Agent in the shell"}


@app.get("/health")
async def health():
    return {"status": "ok"}
