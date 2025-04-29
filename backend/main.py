from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pptx import Presentation
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import io
import os
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables")

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

class FeedbackRequest(BaseModel):
    titles: str
    targetAudience: str

@app.post("/api/get-feedback")
async def get_feedback(request: FeedbackRequest):
    try:
        if not openai.api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")

        prompt = f"""This narrative is intended for {request.targetAudience}.

Content to analyze:
{request.titles}

Please provide feedback on the following:
1. Check if the introduction effectively frames the problem and if the conclusion clearly delivers a strong call to action or takeaway.
2. Identify any points where the transition between slides feels abrupt, confusing, or could be improved.
3. Suggest how to reorganize the slides to make the argument more persuasive."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a presentation structure expert. Analyze the slide titles and provide constructive feedback on the narrative flow."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            feedback = response.choices[0].message.content
            return {"feedback": feedback}
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting feedback from AI service")

    except Exception as e:
        logger.error(f"Unexpected error in get_feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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