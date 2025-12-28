from sqlalchemy.orm import Session
from app.models.user import Movies, MovieAvailability
from sqlalchemy import desc, asc
from typing import Optional, List

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movie_id: int) -> Optional[Movies]:
        return self.db.query(Movies).filter(Movies.id == movie_id).first()

    def create(self, movie: Movies) -> Movies:
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie: Movies) -> Movies:
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie: Movies):
        self.db.delete(movie)
        self.db.commit()

    def list(self, skip: int = 0, limit: int = 20, 
             title: str = None, genre: str = None, 
             language: str = None, rating_from: float = None, 
             sort_by: str = None):
        
        query = self.db.query(Movies).filter(Movies.approved == True) # By default only show approved

        if title:
            query = query.filter(Movies.title.ilike(f"%{title}%"))
        if genre:
            query = query.filter(Movies.genre.ilike(f"%{genre}%"))
        if language:
            query = query.filter(Movies.language == language)
        if rating_from is not None:
            query = query.filter(Movies.rating >= rating_from)

        if sort_by:
            if sort_by == 'release_year_desc':
                query = query.order_by(desc(Movies.release_year))
            elif sort_by == 'rating_desc':
                query = query.order_by(desc(Movies.rating))
            elif sort_by == 'created_at_desc':
                 query = query.order_by(desc(Movies.created_at))
        
        return query.offset(skip).limit(limit).all()

    def add_availability(self, availability: MovieAvailability):
        self.db.add(availability)
        self.db.commit()
        self.db.refresh(availability)
        return availability
