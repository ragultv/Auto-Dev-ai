from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import prompts, agents, execution, evaluation
from app.config import settings

app = FastAPI(
    title="Auto-Dev-ai Backend",
    description="Backend API for Auto-Dev-ai platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prompts.router, prefix="/api/v1/prompts", tags=["prompts"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(execution.router, prefix="/api/v1/execution", tags=["execution"])
app.include_router(evaluation.router, prefix="/api/v1/evaluation", tags=["evaluation"])

@app.get("/")
async def root():
    return {"message": "Auto-Dev-ai Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 