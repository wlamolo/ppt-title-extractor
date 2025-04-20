from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pptx import Presentation
import io
import os

app = FastAPI()

# Serve static files from the frontend build
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets")

# Serve the React app at the root
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse("../frontend/dist/index.html")

# API endpoints under /api prefix
@app.post("/api/extract-titles")
async def extract_titles(file: UploadFile = File(...)):
    # Read the uploaded file
    content = await file.read()
    pptx = Presentation(io.BytesIO(content))
    
    # Extract titles from slides
    titles = []
    for slide in pptx.slides:
        if slide.shapes.title and slide.shapes.title.text:
            titles.append(slide.shapes.title.text)
        else:
            titles.append("[No Title]")
    
    # Create a text file with the titles, adding bold markdown and newlines
    titles_text = "\n".join(f"**Page {i+1}**: {title}" for i, title in enumerate(titles))
    
    return {"titles": titles_text} 