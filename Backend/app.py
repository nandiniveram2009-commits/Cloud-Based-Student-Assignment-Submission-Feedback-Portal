from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, assignment_routes, submission_routes
from services.cloud_db import engine, Base

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud-Based Student Assignment Submission & Feedback Portal",
    version="1.0.0",
    description="Enterprise-grade cloud education portal backend API."
)

# Enable CORS for Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_routes.router, prefix="/api", tags=["Authentication"])
app.include_router(assignment_routes.router, prefix="/api", tags=["Assignments"])
app.include_router(submission_routes.router, prefix="/api", tags=["Submissions"])

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "service": "assignment-portal-backend"}
