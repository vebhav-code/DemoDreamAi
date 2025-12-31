from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # Full Name
    username = Column(String, unique=True, nullable=True) # Display Name
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, nullable=True) # "explorer" or "guide" 
    
    # Profile Details
    mobile_number = Column(String, nullable=True)
    dob = Column(String, nullable=True) # ISO Format YYYY-MM-DD
    gender = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state_city = Column(String, nullable=True)
    qualification_score = Column(String, nullable=True) # e.g. "CGPA 9.0" or "85%"
    
    # Settings / Meta
    profile_photo = Column(String, nullable=True) # URL strings
    timezone = Column(String, nullable=True)
    language = Column(String, default="English")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Performance(Base):
    __tablename__ = "performance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    career = Column(String)
    score = Column(Float)
    test_name = Column(String, nullable=True)  # Name of the test
    difficulty = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")

class TrainingProgress(Base):
    __tablename__ = "training_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Phase: "basic" (15 days), "intermediate" (15 days), "expert" (30 days), "real_world" (6 mos), "completed"
    current_phase = Column(String, default="basic") 
    
    # Day number in the current phase (1-indexed)
    current_day = Column(Integer, default=1)
    
    # Status of the current day: "pending", "submitted", "completed"
    day_status = Column(String, default="pending")
    
    # The task generated for this specific day
    current_task = Column(String, nullable=True) # Description of what to do
    
    # User's completion proof (text or link)
    submission_text = Column(String, nullable=True)
    
    # AI Feedback/Score for the day
    feedback = Column(String, nullable=True)
    
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")

class GuideProfile(Base):
    __tablename__ = "guide_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Verification
    document_path = Column(String, nullable=True)
    verification_status = Column(String, default="pending") # pending, approved, rejected
    
    # Expertise
    expertise_fields = Column(String, nullable=True) # JSON string of selected fields
    experience_years = Column(String, nullable=True) # JSON string or specific value
    linkedin_url = Column(String, nullable=True)
    
    is_onboarded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")

# --- MENTORSHIP SYSTEM MODELS ---

class MentorshipRequest(Base):
    __tablename__ = "mentorship_requests"
    id = Column(Integer, primary_key=True, index=True)
    explorer_id = Column(Integer, ForeignKey("users.id"))
    field = Column(String) # The career field
    title = Column(String)
    description = Column(String)
    status = Column(String, default="open") # open, accepted, solved
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    explorer = relationship("User", foreign_keys=[explorer_id])

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("mentorship_requests.id"))
    explorer_id = Column(Integer, ForeignKey("users.id"))
    guide_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    request = relationship("MentorshipRequest")
    explorer = relationship("User", foreign_keys=[explorer_id])
    guide = relationship("User", foreign_keys=[guide_id])

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
class Guide(Base):
    __tablename__ = "guides"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String) # Hashed or plain for demo
    primary_domain = Column(String)
    years_experience = Column(Integer)
    current_role = Column(String)
    organization = Column(String)
    linkedin_portfolio_url = Column(String)
    bio = Column(String)
    weekly_availability = Column(String)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DreamProject(Base):
    __tablename__ = "dream_projects"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    tech_preference = Column(String, nullable=True)
    skill_level = Column(String) # Beginner, Intermediate, Advanced
    image_path = Column(String, nullable=True)
    roadmap = Column(String, nullable=True) # JSON string from AI
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User")

class ProjectComment(Base):
    __tablename__ = "project_comments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("dream_projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    project = relationship("DreamProject")
    user = relationship("User")
