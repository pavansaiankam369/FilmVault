from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import Movies, MovieAvailability
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieUpdate, MovieAvailabilityCreate

class MovieService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MovieRepository(db)

    def create_movie(self, movie_data: MovieCreate, creator_id: int):
        # Optional: Check if movie already exists by title and year
        # existing = self.db.query(Movies).filter(Movies.title == movie_data.title, Movies.release_year == movie_data.release_year).first()
        # if existing:
        #     raise HTTPException(status_code=400, detail="Movie already exists")

        new_movie = Movies(
            title=movie_data.title,
            description=movie_data.description,
            genre=movie_data.genre,
            language=movie_data.language,
            director=movie_data.director,
            cast=movie_data.cast,
            release_year=movie_data.release_year,
            poster_url=movie_data.poster_url,
            created_by=creator_id,
            approved=False # Default false, admin must approve
        )
        return self.repo.create(new_movie)

    def get_movie(self, movie_id: int):
        movie = self.repo.get_by_id(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie

    def update_movie(self, movie_id: int, movie_data: MovieUpdate):
        movie = self.get_movie(movie_id)
        
        update_data = movie_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(movie, key, value)
            
        return self.repo.update(movie)

    def delete_movie(self, movie_id: int):
        movie = self.get_movie(movie_id)
        self.repo.delete(movie)
        return {"message": "Movie deleted successfully"}

    def list_movies(self, skip: int, limit: int, title: str, genre: str, language: str, rating_from: float, sort_by: str):
        return self.repo.list(skip, limit, title, genre, language, rating_from, sort_by)

    def add_availability(self, movie_id: int, data: MovieAvailabilityCreate):
        self.get_movie(movie_id) # Validate movie exists
        availability = MovieAvailability(
            movie_id=movie_id,
            platform_id=data.platform_id,
            region_id=data.region_id,
            availability_type=data.availability_type,
            start_date=data.start_date,
            end_date=data.end_date,
            url=data.url
        )
        return self.repo.add_availability(availability)

    def approve_movie(self, movie_id: int):
        movie = self.get_movie(movie_id)
        movie.approved = True
        return self.repo.update(movie)
