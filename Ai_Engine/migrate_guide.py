from sqlalchemy import create_engine
from models import Base
from database import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def migrate():
    # This will create tables if they don't exist
    # Since we added GuideProfile, this should create it.
    # It won't affect existing tables unless we drop them (which we won't).
    Base.metadata.create_all(bind=engine)
    print("Database migration complete: GuideProfile table created if not exists.")

if __name__ == "__main__":
    migrate()
