from sqlalchemy import create_engine
from models import Base
from database import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def migrate():
    # MentorshipRequest, ChatSession, Message tables
    Base.metadata.create_all(bind=engine)
    print("Database migration complete: Mentorship tables created.")

if __name__ == "__main__":
    migrate()
