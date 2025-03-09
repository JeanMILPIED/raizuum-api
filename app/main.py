from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routes import ocr, auth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="OCR API", description="An API to extract and analyze text from CV in PDFs.")

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(ocr.router, prefix="/ocr", tags=["OCR"])

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the OCR API!"}

# Run the app when executed directly
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
