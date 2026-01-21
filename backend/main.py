"""
Main FastAPI application for Voice-First Travel Planning Assistant
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv

# Try to load .env, continue if it fails
try:
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except Exception:
    pass  # Continue without .env

# Import modules
from orchestration.planning_pipeline import PlanningPipeline
from evaluations import FeasibilityEval, EditCorrectnessEval, GroundingEval
from email_sender import EmailSender

app = FastAPI(
    title="Voice-First Travel Planning Assistant",
    description="Capstone-grade travel planning with feasibility reasoning",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pipeline = PlanningPipeline(use_mock_data=False)  # Use real OpenStreetMap data
feasibility_eval = FeasibilityEval()
edit_eval = EditCorrectnessEval()
grounding_eval = GroundingEval()

# Initialize email sender (optional - will fail gracefully if not configured)
try:
    email_sender = EmailSender()
except Exception as e:
    email_sender = None
    print(f"Email sender not configured: {e}")

# Store current itinerary in memory (for demo)
current_state = {
    "itinerary": None,
    "constraints": None,
    "pois": [],
    "explanations": []
}


# Request/Response Models
class PlanRequest(BaseModel):
    user_input: str


class EditRequest(BaseModel):
    edit_command: str


class ExplainRequest(BaseModel):
    question: str


class EmailRequest(BaseModel):
    recipient_emails: Optional[List[str]] = None  # Optional, defaults to hardcoded receiver
    subject: Optional[str] = "Your Travel Itinerary from Voyage"


class EditEvalRequest(BaseModel):
    original: Dict[str, Any]
    edited: Dict[str, Any]
    edit_request: Dict[str, Any]
    changes: List[Dict[str, Any]]


# Routes
@app.get("/")
async def root():
    return {
        "message": "Voice-First Travel Planning Assistant API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "planning": "/api/plan",
            "edit": "/api/edit",
            "explain": "/api/explain",
            "evaluations": "/api/eval/*"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/plan")
async def create_plan(request: PlanRequest):
    """
    Create or continue planning based on voice input
    """
    try:
        result = pipeline.handle_user_input(request.user_input)
        
        if result["action"] == "itinerary":
            # Store current state
            current_state["itinerary"] = result["itinerary"]
            current_state["constraints"] = pipeline.collected_constraints
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/edit")
async def edit_plan(request: EditRequest):
    """
    Edit itinerary based on voice command
    """
    try:
        if not current_state["itinerary"]:
            return {
                "action": "error",
                "message": "No itinerary to edit. Please create a plan first."
            }
        
        result = pipeline.handle_edit(
            request.edit_command,
            current_state["itinerary"]
        )
        
        if result["action"] == "edit_applied":
            current_state["itinerary"] = result["itinerary"]
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/explain")
async def explain_plan(request: ExplainRequest):
    """
    Answer questions about the plan
    """
    try:
        result = pipeline.explain(request.question)
        
        # Store explanation for grounding eval
        current_state["explanations"].append(result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/itinerary")
async def get_current_itinerary():
    """
    Get current itinerary
    """
    if not current_state["itinerary"]:
        return {"itinerary": None, "message": "No itinerary created yet"}
    
    return {
        "itinerary": current_state["itinerary"],
        "constraints": current_state["constraints"]
    }


@app.post("/api/eval/feasibility")
async def run_feasibility_eval():
    """
    Run feasibility evaluation on current itinerary
    """
    if not current_state["itinerary"]:
        raise HTTPException(status_code=400, detail="No itinerary to evaluate")
    
    result = feasibility_eval.run(
        current_state["itinerary"],
        current_state["constraints"] or {}
    )
    
    return result


@app.post("/api/eval/edit")
async def run_edit_eval(request: EditEvalRequest):
    """
    Run edit correctness evaluation
    """
    result = edit_eval.run(
        request.original,
        request.edited,
        request.edit_request,
        request.changes
    )
    return result


@app.post("/api/eval/grounding")
async def run_grounding_eval():
    """
    Run grounding evaluation
    """
    if not current_state["itinerary"]:
        raise HTTPException(status_code=400, detail="No itinerary to evaluate")
    
    result = grounding_eval.run(
        current_state["itinerary"],
        current_state["pois"],
        current_state["explanations"]
    )
    
    return result


@app.get("/api/eval/all")
async def run_all_evals():
    """
    Run all evaluations
    """
    if not current_state["itinerary"]:
        raise HTTPException(status_code=400, detail="No itinerary to evaluate")
    
    results = {
        "feasibility": feasibility_eval.run(
            current_state["itinerary"],
            current_state["constraints"] or {}
        ),
        "grounding": grounding_eval.run(
            current_state["itinerary"],
            current_state["pois"],
            current_state["explanations"]
        )
    }
    
    # Overall summary
    all_passed = all(r["passed"] for r in results.values())
    avg_score = sum(r["score"] for r in results.values()) / len(results)
    
    return {
        "all_passed": all_passed,
        "average_score": avg_score,
        "results": results
    }


@app.post("/api/reset")
async def reset_state():
    """
    Reset current state (for new planning session)
    """
    global pipeline
    pipeline = PlanningPipeline(use_mock_data=False)  # Use real data
    
    current_state["itinerary"] = None
    current_state["constraints"] = None
    current_state["pois"] = []
    current_state["explanations"] = []
    
    return {"message": "State reset successfully"}


@app.post("/api/send-email")
async def send_itinerary_email(request: EmailRequest):
    """
    Send current itinerary via email
    """
    if not current_state["itinerary"]:
        raise HTTPException(status_code=400, detail="No itinerary to send. Please create a plan first.")
    
    if not email_sender:
        raise HTTPException(
            status_code=503,
            detail="Email service not configured. Set SENDER_PASSWORD in .env file (sender email is hardcoded to ashup2707@gmail.com)."
        )
    
    # Use hardcoded receiver email if not provided
    recipient_emails = request.recipient_emails if request.recipient_emails else None
    
    # Validate email formats if provided
    if recipient_emails:
        if len(recipient_emails) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 recipients allowed.")
        
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        for email in recipient_emails:
            if not email_pattern.match(email):
                raise HTTPException(status_code=400, detail=f"Invalid email format: {email}")
    
    try:
        result = email_sender.send_itinerary(
            itinerary=current_state["itinerary"],
            recipient_emails=recipient_emails,
            subject=request.subject
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("BACKEND_PORT", 8000)))
