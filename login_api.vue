from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

app = FastAPI(title="Reunify API", version="1.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secure-key-123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock Database
fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "hashed_password": pwd_context.hash("123456"),
        "disabled": False,
        "last_login": None
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Reunify API Service", 
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "login": "/api/login",
            "docs": "/docs"
        }
    }

@app.post("/api/login", response_model=Token)
async def login(login_data: LoginRequest):
    user = fake_users_db.get(login_data.username)
    
    if not user or not pwd_context.verify(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    fake_users_db[login_data.username]["last_login"] = datetime.utcnow()
    
    access_token = create_access_token(data={"sub": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(
        "login_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
