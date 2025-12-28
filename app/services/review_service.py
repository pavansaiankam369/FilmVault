from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.user import Reviews, Movies
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate, ReviewUpdate

class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReviewRepository(db)

    def _update_movie_rating(self, movie_id: int):
        avg_rating = self.db.query(func.avg(Reviews.rating)).filter(Reviews.movie_id == movie_id).scalar()
        movie = self.db.query(Movies).filter(Movies.id == movie_id).first()
        if movie:
            movie.rating = round(avg_rating, 1) if avg_rating else 0.0
            self.db.commit()

    def create_review(self, review_data: ReviewCreate, user_id: int):
        # Check if user already reviewed this movie
        if self.repo.get_by_user_and_movie(user_id, review_data.movie_id):
            raise HTTPException(status_code=400, detail="You have already reviewed this movie")

        new_review = Reviews(
            movie_id=review_data.movie_id,
            user_id=user_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        created_review = self.repo.create(new_review)
        self._update_movie_rating(review_data.movie_id)
        return created_review

    def get_review(self, review_id: int):
        review = self.repo.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    def update_review(self, review_id: int, review_data: ReviewUpdate, user_id: int):
        review = self.get_review(review_id)
        if review.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this review")
        
        if review_data.rating is not None:
            review.rating = review_data.rating
        if review_data.comment is not None:
            review.comment = review_data.comment
            
        updated_review = self.repo.update(review)
        self._update_movie_rating(review.movie_id)
        return updated_review

    def delete_review(self, review_id: int, user_id: int, is_admin: bool = False):
        review = self.get_review(review_id)
        if review.user_id != user_id and not is_admin:
             raise HTTPException(status_code=403, detail="Not authorized to delete this review")
        
        movie_id = review.movie_id
        self.repo.delete(review)
        self._update_movie_rating(movie_id)
        return {"message": "Review deleted successfully"}

    def list_reviews(self, movie_id: int, skip: int, limit: int, sort_by: str):
        return self.repo.list_by_movie(movie_id, skip, limit, sort_by)
