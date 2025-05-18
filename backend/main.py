from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routes import router

app = FastAPI(title="Meme Site API", description="API для сайту з мемами")

# Дозволення CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Meme Site API"}