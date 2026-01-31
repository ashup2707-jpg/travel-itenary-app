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
        "mcp_tools": ["POI Search (OpenStreetMap)", "Itinerary Builder (time blocks, feasibility)"],
        "endpoints": {
            "planning": "/api/plan",
            "edit": "/api/edit",
            "explain": "/api/explain",
            "send_email": "/api/send-email",
            "itinerary": "/api/itinerary",
            "reset": "/api/reset",
            "evaluations": "/api/eval/feasibility, /api/eval/edit, /api/eval/grounding, /api/eval/all"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health/ready")
async def readiness_check():
    """Check if app is ready for demo: backend, LLM, and optional email."""
    llm_configured = bool(
        os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY") or
        os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY") or
        os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
    )
    return {
        "status": "healthy",
        "ready_for_demo": llm_configured,
        "llm_configured": llm_configured,
        "email_configured": email_sender is not None,
        "message": "Ready for Loom" if llm_configured else "Add GROQ_API_KEY or GEMINI_API_KEY to .env for planning"
    }


@app.post("/api/plan")
async def create_plan(request: PlanRequest):
    """
    Create or continue planning based on voice input
    """
    try:
        result = pipeline.handle_user_input(request.user_input)
        
        if result["action"] == "itinerary":
            # Store current state (pois used for grounding eval)
            current_state["itinerary"] = result["itinerary"]
            current_state["constraints"] = pipeline.collected_constraints
            current_state["pois"] = result.get("pois", [])
        
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
    Answer questions about the plan (e.g. "Why did you pick this place?", "Is this plan doable?", "What if it rains?").
    Uses RAG + itinerary for grounded answers; fallback to RAG-only if LLM fails.
    """
    try:
        result = pipeline.explain(
            request.question,
            itinerary=current_state.get("itinerary")
        )
        if result.get("action") == "error":
            return result
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
        # Return result body so frontend can show specific error (auth vs connection vs smtp)
        if result["success"]:
            return result
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Railway uses PORT, but we also support BACKEND_PORT for local dev
    port = int(os.getenv("PORT", os.getenv("BACKEND_PORT", 8000)))
    uvicorn.run(app, host="0.0.0.0", port=port)
