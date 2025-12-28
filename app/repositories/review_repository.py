from sqlalchemy.orm import Session
from app.models.user import Reviews, Movies
from sqlalchemy import desc
from typing import Optional

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, review_id: int) -> Optional[Reviews]:
        return self.db.query(Reviews).filter(Reviews.id == review_id).first()

    def get_by_user_and_movie(self, user_id: int, movie_id: int) -> Optional[Reviews]:
        return self.db.query(Reviews).filter(Reviews.user_id == user_id, Reviews.movie_id == movie_id).first()

    def create(self, review: Reviews) -> Reviews:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def update(self, review: Reviews) -> Reviews:
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete(self, review: Reviews):
        self.db.delete(review)
        self.db.commit()

    def list_by_movie(self, movie_id: int, skip: int = 0, limit: int = 20, sort_by: str = None):
        query = self.db.query(Reviews).filter(Reviews.movie_id == movie_id)
        if sort_by == 'rating_desc':
            query = query.order_by(desc(Reviews.rating))
        else:
             query = query.order_by(desc(Reviews.created_at))
        return query.offset(skip).limit(limit).all()
