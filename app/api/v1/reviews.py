from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import SessionLocal
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.services.review_service import ReviewService
from app.api.v1.auth import get_current_user, get_db
from app.models.user import User
from app.api.v1.platforms import get_current_admin

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse, status_code=201)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ReviewService(db)
    return service.create_review(review, current_user.id)

@router.get("/by-movie/{movie_id}", response_model=List[ReviewResponse])
def list_reviews(
    movie_id: int,
    skip: int = 0, 
    limit: int = 20, 
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = ReviewService(db)
    return service.list_reviews(movie_id, skip, limit, sort_by)

@router.put("/{id}", status_code=204)
def update_review(id: int, review: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ReviewService(db)
    service.update_review(id, review, current_user.id)
    return

@router.delete("/{id}", status_code=204)
def delete_review(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ReviewService(db)
    # Check if admin to allow override
    is_admin = current_user.role == 'admin'
    service.delete_review(id, current_user.id, is_admin)
    return
