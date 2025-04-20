from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pptx import Presentation
import io
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        # Log request received
        logger.info(f"Received file: {file.filename}")
        
        # Verify file type
        if not file.filename.endswith('.pptx'):
            logger.error(f"Invalid file type: {file.filename}")
            raise HTTPException(status_code=400, detail="File must be a .pptx file")
        
        # Read the uploaded file
        try:
            content = await file.read()
            if not content:
                logger.error("Empty file received")
                raise HTTPException(status_code=400, detail="Empty file uploaded")
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise HTTPException(status_code=400, detail="Could not read the uploaded file")
            
        # Create presentation object
        try:
            pptx = Presentation(io.BytesIO(content))
        except Exception as e:
            logger.error(f"Error creating Presentation object: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid PowerPoint file format")
        
        # Extract titles from slides
        titles = []
        for i, slide in enumerate(pptx.slides):
            try:
                if slide.shapes.title and slide.shapes.title.text:
                    titles.append(slide.shapes.title.text.strip())
                    logger.info(f"Extracted title from slide {i+1}: {titles[-1]}")
                else:
                    titles.append("[No Title]")
                    logger.info(f"No title found in slide {i+1}")
            except Exception as e:
                logger.error(f"Error processing slide {i+1}: {str(e)}")
                titles.append(f"[Error processing slide {i+1}]")
        
        if not titles:
            logger.warning("No slides found in presentation")
            return {"titles": "No slides found in the presentation"}
        
        # Create a text file with the titles
        titles_text = "\n".join(f"**Page {i+1}**: {title}" for i, title in enumerate(titles))
        
        logger.info(f"Successfully processed {len(titles)} slides")
        return {"titles": titles_text}
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 