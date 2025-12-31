from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

import models
from database import engine, get_db, init_db
from generator import generate_questions, chat_response, generate_daily_task, grade_submission, generate_project_roadmap, generate_simulation_response
from guide_system import router as guide_router
import json
from sqlalchemy.exc import IntegrityError

# Initialize Database
init_db()

app = FastAPI()

# Include Guide System Routes
app.include_router(guide_router)

# Input Schemas
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class UserSignup(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "explorer"

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # Format history for the generator
    # Ensure history is a list of {"role": "user"|"assistant", "content": "..."}
    response = chat_response(req.message, req.history)
    return {"reply": response}

class QuizRequest(BaseModel):
    field: str
    difficulty: str

@app.post("/generate")
async def generate_quiz_endpoint(req: QuizRequest):
    questions_data = generate_questions(req.field, req.difficulty)
    return {"questions": questions_data}

class UserLogin(BaseModel):
    email: str
    password: str

# --- Auth Routes ---
@app.post("/signup")
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password, # Plaintext for demo
        username=user.email, # Use email as username for uniqueness
        role=user.role
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # If guide, create profile entry
        if user.role == "guide":
            profile = models.GuideProfile(user_id=new_user.id)
            db.add(profile)
            
            # Also create an entry in the primary 'guides' table for discovery
            guide = models.Guide(
                user_id=new_user.id,
                full_name=user.name,
                email=user.email,
                password=user.password,
                verified=False
            )
            db.add(guide)
            db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed. Email or Username might already exist.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role
        }
    }

class UserRoleUpdate(BaseModel):
    email: str
    role: str

@app.post("/set_role")
async def set_user_role(update: UserRoleUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == update.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = update.role
    db.commit()
    return {"message": "Role updated successfully"}

@app.get("/profile/{email}")
async def get_profile_details(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "mobile_number": user.mobile_number,
        "dob": user.dob,
        "gender": user.gender,
        "country": user.country,
        "state_city": user.state_city,
        "qualification_score": user.qualification_score,
        "timezone": user.timezone,
        "language": user.language,
        "created_at": user.created_at,
        "account_status": "Active" if user.is_active else "Inactive"
    }

# --- Guide Onboarding ---
class GuideUpdate(BaseModel):
    email: str
    linkedin_url: Optional[str] = None
    expertise_fields: List[str] = []

@app.get("/guide/status/{email}")
async def get_guide_status(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    profile = db.query(models.GuideProfile).filter(models.GuideProfile.user_id == user.id).first()
    
    if not profile:
        # Create empty profile if not exists
        profile = models.GuideProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
    return {
        "is_onboarded": profile.is_onboarded,
        "verification_status": profile.verification_status,
        "expertise": profile.expertise_fields
    }

@app.post("/guide/onboard")
async def guide_onboard(data: GuideUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    profile = db.query(models.GuideProfile).filter(models.GuideProfile.user_id == user.id).first()
    if not profile:
         profile = models.GuideProfile(user_id=user.id)
         db.add(profile)
    
    # Update Fields
    profile.expertise_fields = json.dumps(data.expertise_fields)
    profile.linkedin_url = data.linkedin_url
    profile.is_onboarded = True # Mark as done for this demo
    
    db.commit()
    return {"message": "Onboarding complete"}

# --- Mentorship & Chat System ---
class MentorshipSubmit(BaseModel):
    email: str
    field: str
    title: str
    description: str

@app.post("/mentorship/request")
async def create_mentorship_request(req: MentorshipSubmit, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    
    new_req = models.MentorshipRequest(
        explorer_id=user.id,
        field=req.field,
        title=req.title,
        description=req.description
    )
    db.add(new_req)
    db.commit()
    return {"message": "Request submitted successfully"}

@app.get("/mentorship/available/{email}")
async def get_available_requests(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user: return []
    guide_profile = db.query(models.GuideProfile).filter(models.GuideProfile.user_id == user.id).first()
    if not guide_profile: return []
    
    try:
        expertise = json.loads(guide_profile.expertise_fields) if guide_profile.expertise_fields else []
    except:
        expertise = []
    
    # Normalize expertise
    expertise = [e.strip().lower() for e in expertise if isinstance(e, str)]
    
    all_requests = db.query(models.MentorshipRequest).filter(
        models.MentorshipRequest.status == "open"
    ).all()
    
    # Client-side filtering for better debugging and robustness
    matching_requests = []
    for r in all_requests:
        if r.field.strip().lower() in expertise:
            matching_requests.append(r)
    
    return [{
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "field": r.field,
        "explorer_name": r.explorer.name if r.explorer else "Unknown",
        "created_at": r.created_at
    } for r in matching_requests]

class AcceptRequest(BaseModel):
    guide_email: str
    request_id: int

@app.post("/mentorship/accept")
async def accept_mentorship_request(data: AcceptRequest, db: Session = Depends(get_db)):
    guide = db.query(models.User).filter(models.User.email == data.guide_email).first()
    req = db.query(models.MentorshipRequest).filter(models.MentorshipRequest.id == data.request_id).first()
    
    if not req:
        raise HTTPException(status_code=404, detail="Mentorship request not found")
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
        
    if req.status != "open":
        raise HTTPException(status_code=400, detail="Request already accepted or closed")
    
    req.status = "accepted"
    
    # Create Chat Session
    session = models.ChatSession(
        request_id=req.id,
        explorer_id=req.explorer_id,
        guide_id=guide.id
    )
    db.add(session)
    db.commit()
    return {"session_id": session.id}

@app.get("/chat/sessions/{email}")
async def get_user_chat_sessions(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user: return []
    sessions = db.query(models.ChatSession).filter(
        (models.ChatSession.explorer_id == user.id) | (models.ChatSession.guide_id == user.id)
    ).all()
    
    return [{
        "id": s.id,
        "explorer_name": s.explorer.name if s.explorer else "Unknown",
        "guide_name": s.guide.name if s.guide else "Unknown",
        "field": s.request.field if s.request else "General",
        "title": s.request.title if s.request else "Chat Session"
    } for s in sessions]

class MessageSend(BaseModel):
    session_id: int
    sender_email: str
    content: str

@app.post("/chat/send")
async def send_message(msg: MessageSend, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == msg.sender_email).first()
    new_msg = models.Message(
        session_id=msg.session_id,
        sender_id=user.id,
        content=msg.content
    )
    db.add(new_msg)
    db.commit()
    return {"status": "sent"}

@app.get("/chat/messages/{session_id}")
async def get_messages(session_id: int, db: Session = Depends(get_db)):
    msgs = db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.timestamp.asc()).all()
    return [{
        "sender_id": m.sender_id,
        "content": m.content,
        "timestamp": m.timestamp
    } for m in msgs]

# --- DREAM TRAINING SYSTEM ---

class TrainingSubmission(BaseModel):
    email: str
    submission_text: str

@app.get("/training/status/{email}")
async def get_training_status(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if entry exists
    progress = db.query(models.TrainingProgress).filter(models.TrainingProgress.user_id == user.id).first()
    
    if not progress:
        # Create initial entry
        progress = models.TrainingProgress(user_id=user.id)
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return {
        "phase": progress.current_phase,
        "day": progress.current_day,
        "status": progress.day_status,
        "task": progress.current_task,
        "feedback": progress.feedback
    }

@app.post("/training/generate_task/{email}")
async def start_daily_task(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    progress = db.query(models.TrainingProgress).filter(models.TrainingProgress.user_id == user.id).first()
    
    if not progress:
        raise HTTPException(status_code=400, detail="Initialize training first")
    
    if progress.current_task and progress.day_status == "pending":
        return {"message": "Task already exists", "task": progress.current_task}
    
    # Generate new task
    task_data = generate_daily_task(progress.current_phase, progress.current_day)
    
    # Store as string (JSON dumps)
    progress.current_task = json.dumps(task_data)
    progress.day_status = "pending"
    progress.submission_text = None
    progress.feedback = None
    db.commit()
    
    return task_data

@app.post("/training/submit")
async def submit_daily_task(sub: TrainingSubmission, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == sub.email).first()
    progress = db.query(models.TrainingProgress).filter(models.TrainingProgress.user_id == user.id).first()
    
    if not progress or not progress.current_task:
        raise HTTPException(status_code=400, detail="No active task")
        
    grade = grade_submission(progress.current_task, sub.submission_text)
    
    progress.submission_text = sub.submission_text
    progress.feedback = grade.get("feedback", "Recorded.")
    
    if grade.get("passed", False):
        progress.day_status = "completed"
        # Logic to advance
        
        # Max days per phase
        max_days = {
            "basic": 15,
            "intermediate": 15,
            "expert": 30
        }
        
        current_max = max_days.get(progress.current_phase, 15)
        
        if progress.current_day >= current_max:
            # Advance Phase
            if progress.current_phase == "basic":
                progress.current_phase = "intermediate"
                progress.current_day = 1
            elif progress.current_phase == "intermediate":
                progress.current_phase = "expert"
                progress.current_day = 1
            elif progress.current_phase == "expert":
                progress.current_phase = "real_world" # Certificate earned
                progress.current_day = 1
        else:
            progress.current_day += 1
            
        progress.current_task = None # Clear for next day
        
    else:
        progress.day_status = "failed" # Retry needed
        
    db.commit()
    return {"passed": grade.get("passed"), "feedback": progress.feedback, "new_phase": progress.current_phase}

@app.get("/guides/discovery")
async def discover_guides(
    field: Optional[str] = None, 
    min_exp: Optional[int] = 0, 
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    stmt = db.query(models.Guide).filter(models.Guide.verified == True)
    
    if field and field != "All":
        stmt = stmt.filter(models.Guide.primary_domain.ilike(f"%{field}%"))
    
    if min_exp:
        stmt = stmt.filter(models.Guide.years_experience >= min_exp)
        
    if query:
        stmt = stmt.filter(
            (models.Guide.full_name.ilike(f"%{query}%")) | 
            (models.Guide.bio.ilike(f"%{query}%")) |
            (models.Guide.current_role.ilike(f"%{query}%"))
        )
        
    guides = stmt.all()
    
    return [{
        "id": g.id,
        "name": g.full_name,
        "email": g.email,
        "domain": g.primary_domain,
        "experience": g.years_experience,
        "role": g.current_role,
        "org": g.organization,
        "bio": g.bio,
        "verified": g.verified,
        "availability": g.weekly_availability
    } for g in guides]

# --- Performance & User Data ---

class PerformanceSave(BaseModel):
    user_email: str
    career: str
    score: float
    difficulty: str

@app.post("/save-result")
async def save_test_result(data: PerformanceSave, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    perf = models.Performance(
        user_id=user.id,
        career=data.career,
        score=data.score,
        difficulty=data.difficulty
    )
    db.add(perf)
    db.commit()
    return {"message": "Result saved"}

@app.get("/performance/{email}")
async def get_performance(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    history = db.query(models.Performance).filter(models.Performance.user_id == user.id).all()
    
    return {
        "history": [{
            "career": h.career,
            "score": h.score,
            "difficulty": h.difficulty,
            "timestamp": h.timestamp,
            "rank": 1 # Mock rank for demo
        } for h in history],
        "stats": {
            "points": len(history) * 100,
            "global_rank": 120 - len(history) # Mock formula
        }
    }

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    mobile_number: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    state_city: Optional[str] = None
    qualification_score: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None

@app.put("/update-profile/{email}")
async def update_profile(email: str, data: ProfileUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
        
    db.commit()
    return {"message": "Profile updated"}

# --- Admin System ---

@app.get("/admin/pending_guides")
async def get_pending_guides(db: Session = Depends(get_db)):
    # Get all profiles that are pending
    pending = db.query(models.GuideProfile).filter(models.GuideProfile.verification_status == "pending").all()
    
    results = []
    for p in pending:
        user = db.query(models.User).filter(models.User.id == p.user_id).first()
        if user:
            results.append({
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "linkedin": p.linkedin_url,
                "expertise": p.expertise_fields,
                "status": p.verification_status
            })
    return results

class VerifyAction(BaseModel):
    user_id: int
    action: str # "approve" or "reject"

@app.post("/admin/verify_guide")
async def verify_guide(data: VerifyAction, db: Session = Depends(get_db)):
    profile = db.query(models.GuideProfile).filter(models.GuideProfile.user_id == data.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if data.action == "approve":
        profile.verification_status = "approved"
        # Also update the Guide table if it exists
        guide = db.query(models.Guide).filter(models.Guide.user_id == data.user_id).first()
        if guide:
            guide.verified = True
    else:
        profile.verification_status = "rejected"
        guide = db.query(models.Guide).filter(models.Guide.user_id == data.user_id).first()
        if guide:
            guide.verified = False
            
    db.commit()
    return {"message": f"Guide {data.action}d successfully"}

# --- MyDreamProject System ---

class DreamProjectCreate(BaseModel):
    email: str
    description: str
    tech_preference: Optional[str] = ""
    skill_level: str

@app.post("/dream-project/create")
async def create_dream_project(req: DreamProjectCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    roadmap = generate_project_roadmap(req.description, req.tech_preference, req.skill_level)
    
    new_project = models.DreamProject(
        user_id=user.id,
        description=req.description,
        tech_preference=req.tech_preference,
        skill_level=req.skill_level,
        roadmap=json.dumps(roadmap) if roadmap else None
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {
        "id": new_project.id,
        "description": new_project.description,
        "tech_preference": new_project.tech_preference,
        "skill_level": new_project.skill_level,
        "roadmap": roadmap,
        "created_at": new_project.created_at
    }

@app.get("/dream-project/all/{email}")
async def get_user_projects(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return []
    projects = db.query(models.DreamProject).filter(models.DreamProject.user_id == user.id).order_by(models.DreamProject.created_at.desc()).all()
    return [{
        "id": p.id,
        "description": p.description,
        "tech_preference": p.tech_preference,
        "skill_level": p.skill_level,
        "roadmap": json.loads(p.roadmap) if p.roadmap else None,
        "created_at": p.created_at
    } for p in projects]

class ProjectCommentCreate(BaseModel):
    project_id: int
    user_email: str
    content: str

@app.post("/dream-project/comment")
async def add_project_comment(req: ProjectCommentCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    comment = models.ProjectComment(
        project_id=req.project_id,
        user_id=user.id,
        content=req.content
    )
    db.add(comment)
    db.commit()
    return {"message": "Comment added"}

@app.get("/dream-project/comments/{project_id}")
async def get_project_comments(project_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.ProjectComment).filter(models.ProjectComment.project_id == project_id).order_by(models.ProjectComment.timestamp.asc()).all()
    return [{
        "user_name": c.user.name,
        "content": c.content,
        "timestamp": c.timestamp
    } for c in comments]

# --- Real-World Dream Experience Simulator ---

class SimulationRequest(BaseModel):
    role: str
    user_context: str = "" # Empty for first start
    history: List[dict] = [] # [{"role": "assistant", "content": "..."}, {"role": "user", "content": "..."}]

@app.post("/simulate")
async def simulate_experience(req: SimulationRequest):
    # If no history, it's the start
    response_text = generate_simulation_response(req.role, req.user_context, req.history)
    return {"reply": response_text}

