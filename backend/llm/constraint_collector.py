"""
Constraint Collector with Max 6 Questions
LLM-guided constraint collection with symbolic validation
"""
import os
import sys
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.llm_client import LLMClient
from symbolic.question_counter import QuestionCounter

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

class ConstraintCollector:
    """
    Collects user constraints with max 6 clarification questions
    Uses LLM for natural conversation, symbolic validation for hard limits
    """
    
    def __init__(self, use_simple_questions: bool = False):
        self.use_simple_questions = use_simple_questions
        self.question_counter = QuestionCounter(max_questions=6)
        
        if not use_simple_questions:
            try:
                self.llm_client = LLMClient()
            except Exception as e:
                print(f"⚠️ LLM client initialization failed in ConstraintCollector: {e}")
                print("⚠️ Using simple predefined questions")
                self.use_simple_questions = True
    
    def collect(
        self,
        initial_intent: Dict[str, Any],
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Collect constraints from user
        
        Args:
            initial_intent: Initial parsed intent from IntentParser
            conversation_history: Previous conversation turns
        
        Returns:
            Dictionary with action ("ask", "proceed", "max_reached") and data
        """
        if conversation_history is None:
            conversation_history = []
        
        # Check question count (symbolic validation)
        if self.question_counter.is_max_reached():
            return {
                "action": "max_reached",
                "message": "Maximum questions reached. Proceeding with available information.",
                "constraints": self._extract_constraints(initial_intent, conversation_history),
                "question_count": self.question_counter.get_count()
            }
        
        # Identify missing information (LLM)
        missing_info = self._identify_missing(initial_intent)
        
        if not missing_info:
            # All required info present - validate (symbolic)
            if self._validate_constraints(initial_intent):
                return {
                    "action": "proceed",
                    "message": "All constraints collected. Ready to plan!",
                    "constraints": self._extract_constraints(initial_intent, conversation_history),
                    "question_count": self.question_counter.get_count()
                }
            else:
                # Still missing required info
                missing_info = self._get_required_missing(initial_intent)
        
        # Generate question (LLM)
        question = self._generate_question(missing_info, conversation_history)
        
        # Increment counter (symbolic)
        self.question_counter.increment()
        
        return {
            "action": "ask",
            "question": question,
            "missing_info": missing_info,
            "constraints": self._extract_constraints(initial_intent, conversation_history),
            "question_count": self.question_counter.get_count()
        }
    
    def _identify_missing(self, intent: Dict[str, Any]) -> List[str]:
        """Identify missing information"""
        required_fields = ['city', 'duration']
        optional_fields = ['interests']
        
        missing = []
        
        # Check required fields
        for field in required_fields:
            value = intent.get(field)
            if value is None or value == "" or value == []:
                missing.append(field)
        
        # Check optional but important fields
        for field in optional_fields:
            value = intent.get(field)
            if not value or (isinstance(value, list) and len(value) == 0):
                # Only add if we haven't asked many questions yet
                if len(missing) < 2:  # Don't ask too many questions at once
                    missing.append(field)
        
        return missing
    
    def _get_required_missing(self, intent: Dict[str, Any]) -> List[str]:
        """Get required missing fields"""
        required = ['city', 'duration', 'interests']
        missing = []
        for field in required:
            if not intent.get(field):
                missing.append(field)
        return missing
    
    def _validate_constraints(self, intent: Dict[str, Any]) -> bool:
        """Validate all required constraints are present (symbolic validation)"""
        required = ['city', 'duration']
        
        for field in required:
            value = intent.get(field)
            if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                return False
        
        return True
    
    def _generate_question(
        self,
        missing_info: List[str],
        conversation_history: List[Dict]
    ) -> str:
        """Generate natural clarification question"""
        # Use simple predefined questions if LLM is unavailable
        if self.use_simple_questions:
            return self._generate_simple_question(missing_info)
        
        missing_str = ", ".join(missing_info)
        
        prompt = f"""
        Generate a natural, conversational clarification question to ask the user.
        
        Missing information: {missing_str}
        Previous conversation: {conversation_history[-2:] if len(conversation_history) > 1 else "None"}
        
        Ask ONE question about the missing information in a natural, friendly way.
        Keep it short and conversational.
        
        Example:
        Missing: city
        Question: "Which city would you like to visit?"
        
        Missing: duration
        Question: "How many days is your trip?"
        
        Missing: interests
        Question: "What are you interested in? For example, food, culture, history, or nature?"
        """
        
        try:
            response = self.llm_client.call(
                prompt=prompt,
                temperature=0.7,
                max_tokens=100
            )
            return response.strip()
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                print("⚠️ API quota exceeded - using simple questions")
                self.use_simple_questions = True
            return self._generate_simple_question(missing_info)
    
    def _generate_simple_question(self, missing_info: List[str]) -> str:
        """Generate simple predefined question"""
        simple_questions = {
            "city": "Which city would you like to visit?",
            "duration": "How many days is your trip?",
            "interests": "What are you interested in? For example: food, culture, history, or nature?",
            "pace": "What pace do you prefer? (relaxed, moderate, or fast)",
            "dates": "When would you like to travel?"
        }
        
        # Return question for first missing item
        if missing_info:
            first_missing = missing_info[0]
            return simple_questions.get(first_missing, f"Could you provide information about {first_missing}?")
        
        return "Tell me more about your trip preferences."
    
    def _extract_constraints(
        self,
        intent: Dict[str, Any],
        conversation_history: List[Dict]
    ) -> Dict[str, Any]:
        """Extract final constraints from intent and conversation"""
        constraints = {
            "city": intent.get("city"),
            "duration": intent.get("duration"),
            "interests": intent.get("interests", []),
            "pace": intent.get("pace", "moderate"),
            "dates": intent.get("dates"),
            "constraints": intent.get("constraints") or {}
        }
        
        return constraints


# Test function
if __name__ == "__main__":
    collector = ConstraintCollector()
    
    # Test with missing info
    initial_intent = {
        "city": "Jaipur",
        "duration": None,  # Missing
        "interests": ["culture"],
        "pace": "relaxed",
        "missing_info": ["duration"]
    }
    
    print("🔍 Testing Constraint Collector...")
    print(f"Initial intent: {initial_intent}\n")
    
    result = collector.collect(initial_intent)
    
    print(f"Action: {result['action']}")
    print(f"Question: {result.get('question', 'N/A')}")
    print(f"Question count: {result['question_count']}/6")
    print(f"Constraints: {result['constraints']}")
