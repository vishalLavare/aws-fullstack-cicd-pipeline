from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.routes import router
except ModuleNotFoundError:
    from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=====================================")
    print(" FastAPI Application Started")
    print(" Environment : Production")
    print("=====================================")
    yield

app = FastAPI(
    title="Production CI/CD FastAPI App",
    description="Automated deployment project built with GitHub Actions, Docker, Amazon ECR, Docker, and EC2.",
    version="1.0.0",
    lifespan=lifespan
)

# ==========================================================
# CORS Configuration
# ==========================================================

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://dpop0vbtqm0t3.cloudfront.net",
    "https://dpop0vbtqm0t3.cloudfront.net",
    "http://demo-1555652099.us-east-1.elb.amazonaws.com:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Register API Routes
# ==========================================================

app.include_router(router, prefix="/api/v1")

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to the Production CI/CD FastAPI Application!",
        "status": "Running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# ==========================================================
# Health Endpoint
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": "production"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)