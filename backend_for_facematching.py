# main.py
import os
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from pymongo import MongoClient, ASCENDING
from deepface import DeepFace
import faiss
import numpy as np
import uuid
from PIL import Image
import io
import logging
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient

# Configuration
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    UPLOAD_DIR = "uploads"
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    FAISS_INDEX_PATH = "faiss_index.index"

# Initialize
app = FastAPI(title="Reunify API", version="1.0")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Models
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Report(BaseModel):
    report_id: str
    name: str
    age: int
    last_seen: str
    datetime_last_seen: datetime
    photo_url: str
    embedding: List[float]
    status: str = "active"
    created_by: str
    created_at: datetime = datetime.utcnow()

# Database Setup
client = AsyncIOMotorClient(Config.MONGODB_URI)
db = client.reunify
users_collection = db.users
reports_collection = db.reports

# FAISS Index
if os.path.exists(Config.FAISS_INDEX_PATH):
    index = faiss.read_index(Config.FAISS_INDEX_PATH)
else:
    index = faiss.IndexFlatL2(128)  # Facenet embedding size
    faiss.write_index(index, Config.FAISS_INDEX_PATH)

# Utility Functions
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await users_collection.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def process_image(file: UploadFile):
    try:
        # Validate
        if file.content_type.split("/")[-1].lower() not in Config.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid image type")
        
        if file.size > Config.MAX_IMAGE_SIZE:
            raise HTTPException(status_code=400, detail="Image too large")
        
        # Optimize
        image = Image.open(io.BytesIO(file.file.read()))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        if max(image.size) > 1600:
            image.thumbnail((1600, 1600))
        
        return image
    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        raise HTTPException(status_code=400, detail="Image processing failed")

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    email: EmailStr = Form(...),
    full_name: str = Form(None)
):
    if await users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = get_password_hash(password)
    user = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "disabled": False
    }
    
    await users_collection.insert_one(user)
    return {"status": "success", "message": "User created"}

@app.post("/api/reports", response_model=Report)
async def create_report(
    name: str = Form(...),
    age: int = Form(...),
    last_seen: str = Form(...),
    datetime_last_seen: str = Form(...),
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    dress_color: Optional[str] = Form(None),
    hair_color: Optional[str] = Form(None),
    height: Optional[int] = Form(None),
    weight: Optional[int] = Form(None),
    face_color: Optional[str] = Form(None),
    details: Optional[str] = Form(None)
):
    try:
        # Process image
        os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
        image = process_image(photo)
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(Config.UPLOAD_DIR, filename)
        image.save(filepath, "JPEG", quality=85)
        
        # Generate embedding
        try:
            embedding = DeepFace.represent(
                img_path=filepath,
                model_name="Facenet",
                detector_backend="mtcnn"
            )[0]["embedding"]
        except ValueError as e:
            if "Face could not be detected" in str(e):
                raise HTTPException(status_code=400, detail="No face detected")
            raise
        
        # Create report
        report = {
            "report_id": str(uuid.uuid4()),
            "name": name.strip(),
            "age": age,
            "last_seen": last_seen.strip(),
            "datetime_last_seen": datetime.fromisoformat(datetime_last_seen),
            "photo_url": f"/uploads/{filename}",
            "embedding": embedding,
            "status": "active",
            "created_by": current_user["username"],
            "created_at": datetime.utcnow(),
            "appearance": {
                "dress_color": dress_color,
                "hair_color": hair_color,
                "height": height,
                "weight": weight,
                "face_color": face_color
            },
            "details": details
        }
        
        # Add to FAISS index
        embedding_array = np.array([embedding], dtype='float32')
        index.add(embedding_array)
        faiss.write_index(index, Config.FAISS_INDEX_PATH)
        
        # Save to DB
        await reports_collection.insert_one(report)
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Report creation failed")

@app.get("/api/reports/search")
async def search_reports(
    photo: UploadFile = File(...),
    threshold: float = 0.7,
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Process image
        temp_path = f"temp_{uuid.uuid4()}.jpg"
        image = process_image(photo)
        image.save(temp_path, "JPEG", quality=85)
        
        # Get embedding
        try:
            query_embedding = DeepFace.represent(
                img_path=temp_path,
                model_name="Facenet"
            )[0]["embedding"]
        except ValueError:
            raise HTTPException(status_code=400, detail="No face detected in query image")
        
        # Search FAISS
        query_array = np.array([query_embedding], dtype='float32')
        distances, indices = index.search(query_array, k=10)
        
        # Get matches
        matches = []
        for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
            if idx == -1 or dist > (1 - threshold):
                continue
            
            report = await reports_collection.find_one(
                {"status": "active"},
                skip=idx,
                projection={"_id": 0, "embedding": 0}
            )
            
            if report:
                matches.append({
                    **report,
                    "similarity": float(1 - dist),
                    "rank": i + 1
                })
        
        os.remove(temp_path)
        return {"matches": matches[:5]}  # Return top 5 matches
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/api/reports", response_model=List[Report])
async def list_reports(
    skip: int = 0,
    limit: int = 10,
    status_filter: str = "active",
    current_user: User = Depends(get_current_active_user)
):
    try:
        cursor = reports_collection.find(
            {"status": status_filter},
            {"_id": 0, "embedding": 0}
        ).sort("created_at", -1).skip(skip).limit(limit)
        
        return await cursor.to_list(length=limit)
    except Exception as e:
        logger.error(f"Failed to fetch reports: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch reports")

@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(
    report_id: str,
    current_user: User = Depends(get_current_active_user)
):
    report = await reports_collection.find_one(
        {"report_id": report_id},
        {"_id": 0, "embedding": 0}
    )
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report

@app.put("/api/reports/{report_id}/status")
async def update_report_status(
    report_id: str,
    new_status: str = Form(...),
    current_user: User = Depends(get_current_active_user)
):
    if new_status not in ["active", "resolved", "archived"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await reports_collection.update_one(
        {"report_id": report_id},
        {"$set": {"status": new_status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {"status": "success", "message": "Status updated"}

# Startup
@app.on_event("startup")
async def startup_db():
    await users_collection.create_index([("username", ASCENDING)], unique=True)
    await users_collection.create_index([("email", ASCENDING)], unique=True)
    await reports_collection.create_index([("report_id", ASCENDING)], unique=True)
    await reports_collection.create_index([("status", ASCENDING)])
    await reports_collection.create_index([("created_at", ASCENDING)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
