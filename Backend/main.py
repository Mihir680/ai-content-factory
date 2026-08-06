from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.api.history import router as history_router
from Backend.api.thumbnail_image import router as thumbnail_image_router
from Backend.api.research import router as research_router
from Backend.api.script import router as script_router
from Backend.api.seo import router as seo_router
from Backend.api.generate import router as generate_router

# Database
from Backend.database.database import engine
from Backend.database.models import Base

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router)
app.include_router(script_router)
app.include_router(seo_router)
app.include_router(generate_router)
app.include_router(thumbnail_image_router)
app.include_router(generate_router)
app.include_router(history_router)
app.include_router(thumbnail_image_router)

@app.get("/")
def home():
    return {"message": "AI Content Factory"}