from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.schemas.watchlist import WatchlistResponse
from app.services.watchlist_service import WatchlistService
from app.api.v1.auth import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.post("/{movie_id}", status_code=201)
def add_to_watchlist(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WatchlistService(db)
    service.add_to_watchlist(current_user.id, movie_id)
    return {"message": "Movie added to watchlist"}

@router.get("/", response_model=List[WatchlistResponse])
def get_watchlist(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WatchlistService(db)
    return service.list_watchlist(current_user.id, skip, limit)

@router.delete("/{movie_id}", status_code=204)
def remove_from_watchlist(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WatchlistService(db)
    service.remove_from_watchlist(current_user.id, movie_id)
    return

@router.get("/{movie_id}/status")
def check_watchlist_status(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = WatchlistService(db)
    return service.check_status(current_user.id, movie_id)
