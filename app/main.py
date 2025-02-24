from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
from pathlib import Path
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile
import os
models.Base.metadata.create_all(bind=engine)
app = FastAPI() #create instance
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return{'message':"welcome to api"}

@app.post('/upload')
async def endpoint(uploaded_file:UploadFile):
    content=await(uploaded_file.read())
    print(content)


UPLOAD_DIR = Path("D:\\api-files")
UPLOAD_DIR.mkdir(exist_ok=True)  # Create the base upload directory

# Function to determine subfolder based on file type
def get_file_category(content_type: str) -> str:
    if content_type.startswith("image/"):
        return "images"
    elif content_type == "application/pdf":
        return "documents"
    elif content_type in [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-powerpoint"
    ]:
        return "presentations"
    else:
        return "others"

@app.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    category = get_file_category(file.content_type)
    category_dir = UPLOAD_DIR / category
    category_dir.mkdir(exist_ok=True)  # Create category folder if not exists

    file_path = category_dir / file.filename  # Save file in category folder
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_location": str(file_path)
    }
@app.get("/uploads")
def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}
@app.get("/upload/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIR / filename  # Use pathlib Path instead of string concatenation
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    return {"error": "File not found"}
@app.get("/uploads/{category}/")
async def list_files(category: str):
    category_dir = UPLOAD_DIR / category
    if not category_dir.exists():
        return {"error": "Category not found"}

    files = [file.name for file in category_dir.iterdir() if file.is_file()]
    return {"category": category, "files": files}
@app.delete("/uploads/{category}/{filename}")
async def delete_file(category: str, filename: str):
    file_path = UPLOAD_DIR / category / filename  # Locate the file

    if file_path.exists() and file_path.is_file():
        file_path.unlink()  # Delete the file
        return {"message": f"File '{filename}' deleted successfully from '{category}'."}
    
    return {"error": "File not found"}
@app.put("/uploads/{category}/{filename}")
async def update_file(category: str, filename: str, file: UploadFile = File(...)):
    category_dir = UPLOAD_DIR / category
    file_path = category_dir / filename  # Path to old file

    if file_path.exists():
        file_path.unlink()  # Delete the old file before updating

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # Save the new file

    return {
        "message": f"File '{filename}' updated successfully in '{category}'",
        "filename": filename,
        "content_type": file.content_type,
        "file_location": str(file_path)
    }