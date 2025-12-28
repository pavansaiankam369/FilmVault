from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.v1 import auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User & Movie API")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import auth, platforms, regions, movies, reviews, watchlist, users

# ... [Keep previous code]

# Include versioned API routers
app.include_router(auth.router, prefix="/api/v1", tags=["Auth & Users"])
app.include_router(platforms.router, prefix="/api/v1", tags=["Platforms"])
app.include_router(regions.router, prefix="/api/v1", tags=["Regions"])
app.include_router(movies.router, prefix="/api/v1", tags=["Movies"])
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])
app.include_router(watchlist.router, prefix="/api/v1", tags=["Watchlist"])
app.include_router(users.router, prefix="/api/v1", tags=["[Admin] Users"])
