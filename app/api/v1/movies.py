from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import SessionLocal
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate, MovieAvailabilityCreate, MovieAvailabilityResponse
from app.services.movie_service import MovieService
from app.api.v1.auth import get_current_user, get_db
from app.models.user import User
from app.api.v1.platforms import get_current_admin

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieResponse, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = MovieService(db)
    return service.create_movie(movie, current_user.id)

@router.get("/", response_model=List[MovieResponse])
def list_movies(
    skip: int = 0, 
    limit: int = 20, 
    title: Optional[str] = None,
    genre: Optional[str] = None,
    language: Optional[str] = None,
    rating_from: Optional[float] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return service.list_movies(skip, limit, title, genre, language, rating_from, sort_by)

@router.get("/{id}", response_model=MovieResponse)
def get_movie(id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movie(id)

@router.put("/{id}", status_code=204)
def update_movie(id: int, movie: MovieUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = MovieService(db)
    service.update_movie(id, movie)
    return

@router.delete("/{id}", status_code=204)
def delete_movie(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = MovieService(db)
    service.delete_movie(id)
    return

@router.post("/{id}/availability", response_model=MovieAvailabilityResponse)
def add_movie_availability(id: int, availability: MovieAvailabilityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = MovieService(db)
    return service.add_availability(id, availability)

@router.put("/{id}/approve", status_code=204)
def approve_movie(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = MovieService(db)
    service.approve_movie(id)
    return
