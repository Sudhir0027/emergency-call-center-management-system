from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, calls, responders, dashboard, users
from .seed import seed_database

app = FastAPI(
    title="Emergency Call Center Management System",
    description="REST API for emergency call intake, priority processing, responder assignment and history.",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    seed_database()

@app.get("/")
def root():
    return {"message": "Emergency Call Center API", "docs": "/swagger"}

app.include_router(auth.router, prefix="/api")
app.include_router(calls.router, prefix="/api")
app.include_router(responders.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(users.router, prefix="/api")
