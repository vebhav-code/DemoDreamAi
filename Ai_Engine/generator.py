import json
import ollama
import re

def generate_questions(field, difficulty):
    prompt = f"""
Generate 10 multiple-choice questions for the career field: "{field}".
Difficulty level: {difficulty}.

If the field contains a specialized sub-topic (e.g., "Engineering - Computer Science"), focus strictly on that sub-topic.
If the difficulty is "advanced" or if it is a secondary round, ask deeper technical questions specific to that specialization.

STRICT RESPONSE FORMAT:
Return ONLY a JSON list of objects. No explanation, no intro text, no markdown code blocks.

Example structure:
[
  {{
    "id": 1,
    "question": "What is the function of...",
    "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
    "correct_answer": "A"
  }}
]

IMPORTANT:
1. Options MUST start with "A. ", "B. ", "C. ", "D. ".
2. The correct_answer MUST be just the letter (A, B, C, or D).
3. Ensure the output is valid JSON.
"""

    try:
        response = ollama.generate(
            model="gemma3:1b",
            prompt=prompt,
            options={
                "temperature": 0.5 # Lower temp for more deterministic formatting
            }
        )

        raw = response.get("response", "")
        print("\n===== RAW AI OUTPUT =====")
        print(raw)
        print("=========================\n")

        # 1. Clean Markdown Code Fences
        raw_clean = re.sub(r'```json\s*', '', raw)
        raw_clean = re.sub(r'```\s*', '', raw_clean)

        # 2. Try JSON extraction
        match = re.search(r'\[.*\]', raw_clean, re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            json_str = raw_clean

        # 3. Parse
        data = json.loads(json_str)
        return data

    except Exception as e:
        print(f"Error generating questions: {e}")
        # Fallback Questions so user isn't stuck
        return [
            {
                "id": 1,
                "question": f"What is a key skill for a {field}?",
                "options": ["A. Communication", "B. Typing", "C. Driving", "D. Sleeping"],
                "correct_answer": "A"
            },
            {
                "id": 2,
                "question": "Which of these is most important in this career?",
                "options": ["A. Speed", "B. Accuracy", "C. Dedication", "D. All of the above"],
                "correct_answer": "D"
            },
            {
                "id": 3,
                "question": "What is the primary goal of this profession?",
                "options": ["A. To make money", "B. To solve problems", "C. To travel", "D. To be famous"],
                "correct_answer": "B"
            }
        ]

def chat_response(user_message, history=[]):
    system_prompt = """
You are an AI Career Guidance Assistant integrated into an educational platform.

IMPORTANT RULES:
- You ONLY handle career discovery and career recommendations.
- You must NOT discuss quizzes, exams, study guides, or any other platform features.
- You must NOT change or interfere with any existing system behavior.
- Stay strictly within career guidance.

CONVERSATION FLOW:
1. Ask ONE clear question at a time.
2. Your goal is to understand the user's:
   - Interests
   - Skills / strengths
   - Personality traits
   - Career goals and constraints
3. Questions should be simple, student-friendly, and practical.
4. Do NOT suggest any career until you have enough information (minimum 8–12 questions).

QUESTION STRATEGY:
- Start with interests.
- Then move to skills and aptitude.
- Then personality and work style.
- End with goals (government/private, stability vs growth, further studies).

ANSWER HANDLING:
- Accept free-text answers.
- If an answer is vague, ask a follow-up question.
- Do not repeat the same question in different words.

FINAL OUTPUT RULES (ONLY AT THE END):
When enough information is collected, respond in EXACTLY this format:

CAREER_ANALYSIS_COMPLETE

Top 3 Career Recommendations:

1. Career Name
   Match Percentage: XX%
   Why it fits:
   - Point 1
   - Point 2
   - Point 3

2. Career Name
   Match Percentage: XX%
   Why it fits:
   - Point 1
   - Point 2

3. Career Name
   Match Percentage: XX%
   Why it fits:
   - Point 1
   - Point 2

Additional Guidance:
- Suggested skills to focus on
- Suggested next steps (courses, preparation, practice)

BEHAVIOR:
- Be neutral, encouraging, and realistic.
- Do NOT guarantee success or salary.
- Do NOT use emojis.
- Keep responses concise and structured.

If career analysis is NOT complete yet, ask the NEXT BEST question only.
"""
    messages = [{"role": "system", "content": system_prompt}]
    
    # Append history
    # History is expected to be [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    if history:
        messages.extend(history)
        
    # Append current message
    messages.append({"role": "user", "content": user_message})

    try:
        response = ollama.chat(
            model="gemma3:1b", # Using a slightly larger/better model if possible, or stick to what was there. 1b might be weak for complex logic. Let's use 1b as it was there.
            messages=messages,
            options={"temperature": 0.7}
        )
        return response['message']['content']
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def generate_daily_task(phase, day, career_interest="General Career Success"):
    prompt = f"""
    Act as a mentor. Create a specific, actionable daily task for a student in their "{phase}" training phase.
    Day: {day}
    Career Goal: {career_interest}

    Phase Context:
    - Basic (1-15 days): Foundations, mindset, basic research.
    - Intermediate (1-15 days): Skill building, simple projects.
    - Expert (1-30 days): Advanced application, case studies.
    
    Output strictly in JSON format:
    {{
        "title": "Short Task Title",
        "description": "2-3 sentences explaining exactly what to do today.",
        "verification_type": "text_reflection" 
    }}
    """
    try:
        response = ollama.generate(
            model="gemma3:1b",
            prompt=prompt,
            options={"temperature": 0.8}
        )
        raw = response.get("response", "")
        # Clean markdown
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
             return json.loads(match.group(0))
        return {"title": f"Day {day} Challenge", "description": raw, "verification_type": "text_reflection"}
    except Exception as e:
        return {"title": "Daily Task", "description": "Research a key topic in your field.", "verification_type": "text_reflection"}

def grade_submission(task, submission):
    prompt = f"""
    You are a strict but fair evaluator.
    Task: {task}
    User Submission: {submission}
    
    Did the user make a genuine effort to complete the task?
    Return ONLY JSON:
    {{
        "passed": true/false,
        "feedback": "One sentence feedback."
    }}
    """
    try:
        response = ollama.generate(
            model="gemma3:1b",
            prompt=prompt,
            options={"temperature": 0.3}
        )
        raw = response.get("response", "")
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
             return json.loads(match.group(0))
        # Fallback if valid JSON isn't found, assume pass if length is decent
        passed = len(submission) > 20
        return {"passed": passed, "feedback": "Good effort!" if passed else "Please provide more detail."}
    except:
        return {"passed": True, "feedback": "Submission recorded."}

def generate_project_roadmap(description, tech_preference, skill_level):
    prompt = f"""
    You are a Project Mentor and Software Architect.
    Help the user transform the following project idea into a clear, beginner-friendly roadmap.

    Project Description: {description}
    Tech Preference: {tech_preference}
    Skill Level: {skill_level}

    STRICT OUTPUT FORMAT (Return ONLY a JSON object with these keys):
    {{
        "project_overview": "Summary of the project idea, domain, and real-world use case.",
        "required_skills_tools": "List of languages, frameworks, and tools needed.",
        "roadmap": [
            {{
                "phase": "Phase 1: Basics & Setup",
                "steps": ["Step 1...", "Step 2..."],
                "explanation": "Simple explanation of this phase."
            }},
            {{
                "phase": "Phase 2: Core Features",
                "steps": ["Step 1...", "Step 2..."],
                "explanation": "Simple explanation."
            }},
            {{
                "phase": "Phase 3: Advanced Logic",
                "steps": ["Step 1...", "Step 2..."],
                "explanation": "Simple explanation."
            }},
            {{
                "phase": "Phase 4: Testing & Deployment",
                "steps": ["Step 1...", "Step 2..."],
                "explanation": "Simple explanation."
            }}
        ],
        "estimated_time": "Time estimate for completion.",
        "common_mistakes": ["Mistake 1", "Mistake 2"]
    }}

    Rules:
    - Use simple, beginner-friendly language.
    - Avoid unnecessary complexity.
    - Focus on educational value.
    - DO NOT generate code.
    """
    try:
        response = ollama.generate(
            model="gemma3:1b",
            prompt=prompt,
            options={"temperature": 0.7}
        )
        raw = response.get("response", "")
        # Clean markdown code fences if any
        raw_clean = re.sub(r'```json\s*', '', raw)
        raw_clean = re.sub(r'```\s*', '', raw_clean)
        
        match = re.search(r'\{.*\}', raw_clean, re.DOTALL)
        if match:
             return json.loads(match.group(0))
        return None
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        return None

def generate_simulation_response(role, user_context, history=[]):
    system_prompt = f"""
You are a REAL-WORLD DREAM EXPERIENCE SIMULATOR.

Your job is to simulate real-life professional experiences so users feel confident,
comfortable, and mentally prepared for their dream role.

You must NOT use fantasy, exaggeration, or unrealistic success.
Everything must feel practical, human, and real.

────────────────────────────────────────
USER CONTEXT
────────────────────────────────────────
Dream Role: {role}
User Level: Beginner
Purpose: Confidence building + real exposure
Simulation Duration: Condensed real-world experience
Environment: Stress-aware, supportive, realistic

────────────────────────────────────────
GLOBAL RULES (VERY IMPORTANT)
────────────────────────────────────────
1. Simulate ONLY ONE situation at a time.
2. Each situation must be realistic and commonly faced in the selected role.
3. Speak like real people in that profession.
4. Ask the user to make a decision before moving forward.
5. Do NOT reveal future situations in advance.
6. Do NOT judge the user harshly.
7. After each decision:
   - Explain the real-world consequence
   - Explain emotional impact
   - Explain professional lesson
8. Keep the tone encouraging but honest.
9. Never say the user failed — say what can improve.
10. No paid tools, no external services, no references to premium systems.

────────────────────────────────────────
SIMULATION FLOW
────────────────────────────────────────
STEP 1: INTRODUCTION (If history is empty)
- Introduce the role and environment
- Explain expectations clearly
- Set mental readiness
- THEN, Present the FIRST situation.

STEP 2: SITUATION LOOP (If history exists)
For every situation:
- Describe the situation clearly (Context: {user_context})
- Add mild pressure (time, people, responsibility)
- Ask the user to choose or type a response

WAIT for user input.

STEP 3: RESPONSE EVALUATION
After user responds:
- Describe what happened
- Explain why it happened
- Show emotional & professional outcome
- Give 1 short improvement tip

Then move to the NEXT situation immediately.

STEP 4: FINAL EVALUATION (ONLY AT END)
Provide:
- Confidence score (0–100)
- Strengths
- Improvement areas
- “How close you are to real-world readiness”
- Encouraging closing message

────────────────────────────────────────
SITUATION DESIGN RULES
────────────────────────────────────────
- Use real workplace language
- Include human behavior (pressure, doubt, confidence)
- Avoid perfect outcomes
- Allow multiple correct approaches
- Never force a single “right” answer
"""

    messages = [{"role": "system", "content": system_prompt}]
    
    if history:
        messages.extend(history)
    
    # If there's new user input, append it (unless it's the very first start)
    if user_context and len(history) > 0:
        messages.append({"role": "user", "content": user_context})
    elif not history:
        # Initial trigger if history is empty
        messages.append({"role": "user", "content": f"Start the simulation for the role of {role}."})

    try:
        response = ollama.chat(
            model="gemma3:1b", 
            messages=messages,
            options={"temperature": 0.7}
        )
        return response['message']['content']
    except Exception as e:
        return f"Simulation Error: {str(e)}"

