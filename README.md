# PowerPoint Slide Title Extractor

This is a fullstack application that allows users to upload PowerPoint (PPTX) files and extract slide titles. The application consists of a React frontend and a FastAPI backend.

## Prerequisites

- Python 3.7+
- Node.js and npm (for development)

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## Usage

1. Open your browser and navigate to http://localhost:5173
2. Click the file input button and select a PPTX file
3. Click "Extract Titles" to process the file
4. The extracted titles will be displayed on the screen
5. Click "Download Titles" to save the titles as a text file

## Features

- Upload PPTX files
- Extract slide titles
- Download results as a text file
- Modern and responsive UI
- Error handling
- Loading states 