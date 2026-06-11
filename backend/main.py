"""FastAPI backend — login endpoint."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Monorepo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    token: str | None = None
    message: str


@app.get("/")
def root():
    return {"service": "monorepo-api", "status": "ok"}


@app.post("/api/login", response_model=LoginResponse)
def login(body: LoginRequest):
    """Simple login endpoint — demo credentials only."""
    if body.username == "admin" and body.password == "admin123":
        return LoginResponse(
            success=True,
            token="demo-token-abc123",
            message="Login successful",
        )
    if body.username == "user" and body.password == "pass123":
        return LoginResponse(
            success=True,
            token="demo-token-def456",
            message="Login successful",
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")
