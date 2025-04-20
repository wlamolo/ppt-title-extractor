# PowerPoint Slide Title Extractor

A fullstack application that allows users to upload PowerPoint (PPTX) files and extract slide titles. Built with React frontend and FastAPI backend.

## Features

- Upload PPTX files
- Extract slide titles
- Download results as a text file
- Modern, Craigslist-inspired UI
- Error handling
- Loading states

## Prerequisites

- Python 3.7+
- Node.js and npm

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/ppt-title-extractor.git
cd ppt-title-extractor
```

2. Start both servers with a single command:
```bash
./start.sh
```

The application will be available at http://localhost:5175

## Manual Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
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

## Development Scripts

- `start.sh`: Starts both frontend and backend servers
- `stop.sh`: Stops all running servers
- `build.sh`: Builds the project for production

## Deployment

This application can be deployed as a single unit using platforms like:

1. Render.com (Recommended):
   - Fork this repository
   - Create a new Web Service on Render
   - Connect your GitHub repository
   - Use `build.sh` as the build command

2. DigitalOcean App Platform:
   - Fork this repository
   - Create a new App
   - Connect your GitHub repository
   - Use `build.sh` as the build command

## Project Structure

```
ppt-title-extractor/
├── backend/              # FastAPI backend
│   ├── main.py          # Main API endpoints
│   └── requirements.txt  # Python dependencies
├── frontend/            # React frontend
│   ├── src/             # Source code
│   └── package.json     # Node.js dependencies
├── start.sh            # Start development servers
├── stop.sh            # Stop all servers
├── build.sh           # Production build script
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 