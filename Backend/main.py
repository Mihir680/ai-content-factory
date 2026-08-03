from fastapi import FastAPI
from Backend.agents.research import get_business_topics

app = FastAPI(
    title="AI Content Factory",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Content Factory 🚀"
    }

@app.get("/topics")
def get_topics():
    return {
        "topics": get_business_topics()
    }