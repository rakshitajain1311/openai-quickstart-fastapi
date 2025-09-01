from openai import OpenAI
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()

if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = OpenAI(api_key=settings.OPENAI_API_KEY)

app = FastAPI(title="Animal Superhero Name Generator API")

class AnimalRequest(BaseModel):
    animal: str

class SuperheroResponse(BaseModel):
    animal: str
    names: str
    success: bool
    error: str = None

def generate_prompt(animal: str) -> str:
    """Generate prompt for OpenAI API"""
    return f"""Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline

Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot

Animal: {animal.capitalize()}
Names:"""

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Animal Superhero Name Generator API",
        "endpoints": {
            "POST /generate": "Generate superhero names for an animal",
            "GET /generate/{animal}": "Generate names via URL parameter",
            "GET /health": "Health check"
        }
    }

@app.post("/generate", response_model=SuperheroResponse)
async def generate_names_post(request: AnimalRequest):
    """Generate superhero names via POST request"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a creative assistant that generates fun superhero names for animals."},
                {"role": "user", "content": generate_prompt(request.animal)}
            ],
            temperature=0.6,
            max_tokens=100
        )
        
        result = response.choices[0].message.content.strip()
        
        return SuperheroResponse(
            animal=request.animal,
            names=result,
            success=True
        )
        
    except Exception as e:
        return SuperheroResponse(
            animal=request.animal,
            names="",
            success=False,
            error=str(e)
        )

@app.get("/generate/{animal}", response_model=SuperheroResponse)
async def generate_names_get(animal: str):
    """Generate superhero names via GET request"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a creative assistant that generates fun superhero names for animals."},
                {"role": "user", "content": generate_prompt(animal)}
            ],
            temperature=0.6,
            max_tokens=100
        )
        
        result = response.choices[0].message.content.strip()
        
        return SuperheroResponse(
            animal=animal,
            names=result,
            success=True
        )
        
    except Exception as e:
        return SuperheroResponse(
            animal=animal,
            names="",
            success=False,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Animal Superhero Name Generator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050)