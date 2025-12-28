from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models.user import User, Platforms, Regions, Movies, Reviews, MovieAvailability
from app.core.security import hash_password
from datetime import date

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # 1. Seed Users
        if not db.query(User).filter(User.email == "admin@example.com").first():
            admin = User(
                username="Admin User",
                email="admin@example.com",
                role="admin",
                password=hash_password("Admin@123"), # Strong password
                status="active"
            )
            db.add(admin)
            print("Created Admin User")
        
        if not db.query(User).filter(User.email == "user@example.com").first():
            user = User(
                username="Regular User",
                email="user@example.com",
                role="user",
                password=hash_password("User@123"),
                status="active"
            )
            db.add(user)
            print("Created Regular User")
        
        db.commit()

        # Get IDs
        admin_id = db.query(User).filter(User.email == "admin@example.com").first().id
        user_id = db.query(User).filter(User.email == "user@example.com").first().id

        # 2. Seed Platforms
        platforms = [
            {"name": "Netflix", "type": "OTT", "website": "https://netflix.com"},
            {"name": "Amazon Prime", "type": "OTT", "website": "https://primevideo.com"},
            {"name": "PVR Cinemas", "type": "Theater", "website": "https://pvrcinemas.com"},
        ]
        for p in platforms:
            if not db.query(Platforms).filter(Platforms.name == p["name"]).first():
                db.add(Platforms(**p))
                print(f"Created Platform: {p['name']}")
        db.commit()

        # 3. Seed Regions
        regions = [
            {"name": "India", "code": "IN"},
            {"name": "United States", "code": "US"},
            {"name": "United Kingdom", "code": "UK"},
        ]
        for r in regions:
            if not db.query(Regions).filter(Regions.code == r["code"]).first():
                db.add(Regions(**r))
                print(f"Created Region: {r['name']}")
        db.commit()

        # 4. Seed Movies
        movies_data = [
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "genre": "Sci-Fi",
                "language": "English",
                "director": "Christopher Nolan",
                "release_year": 2010,
                "rating": 8.8,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"
            },
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "genre": "Action",
                "language": "English",
                "director": "Christopher Nolan",
                "release_year": 2008,
                "rating": 9.0,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg"
            },
            {
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "genre": "Sci-Fi",
                "language": "English",
                "director": "Christopher Nolan",
                "release_year": 2014,
                "rating": 8.6,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg"
            },
            {
                "title": "Parasite",
                "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                "genre": "Thriller",
                "language": "Korean",
                "director": "Bong Joon Ho",
                "release_year": 2019,
                "rating": 8.5,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
            },
            {
                "title": "The Shawshank Redemption",
                "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "genre": "Drama",
                "language": "English",
                "director": "Frank Darabont",
                "release_year": 1994,
                "rating": 9.3,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"
            },
            {
                "title": "Avengers: Endgame",
                "description": "After the devastating events of Infinity War, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
                "genre": "Superhero",
                "language": "English",
                "director": "Anthony & Joe Russo",
                "release_year": 2019,
                "rating": 8.4,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
            },
            {
                "title": "Joker",
                "description": "A mentally troubled comedian embarks on a downward spiral that leads to the creation of the iconic villain known as The Joker.",
                "genre": "Crime",
                "language": "English",
                "director": "Todd Phillips",
                "release_year": 2019,
                "rating": 8.4,
                "approved": True,
                "created_by": admin_id,
                "poster_url": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"
            }
        ]


        for m_data in movies_data:
            if not db.query(Movies).filter(Movies.title == m_data["title"]).first():
                movie = Movies(**m_data)
                db.add(movie)
                db.commit()
                db.refresh(movie)
                print(f"Created Movie: {movie.title}")

                # Add dummy review
                review = Reviews(
                    movie_id=movie.id,
                    user_id=user_id,
                    rating=9.0,
                    comment="Absolutely fantastic movie!",
                )
                db.add(review)
        db.commit()

        print("Seeding Complete!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
