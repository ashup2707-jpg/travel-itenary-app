"""
LLM Intent Parser
Parses user voice input into structured intent
"""
import os
import sys
from typing import Dict, Optional, Any
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.llm_client import LLMClient
from llm.simple_intent_parser import SimpleIntentParser

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

class IntentParser:
    """
    Parses user voice input into structured intent
    Uses LLM when available, falls back to rule-based parser
    """
    
    def __init__(self, use_simple_parser: bool = False):
        self.use_simple_parser = use_simple_parser
        self.simple_parser = SimpleIntentParser()
        
        if not use_simple_parser:
            try:
                self.llm_client = LLMClient()
            except Exception as e:
                print(f"⚠️ LLM client initialization failed: {e}")
                print("⚠️ Falling back to simple rule-based parser")
                self.use_simple_parser = True
    
    def parse(self, user_input: str) -> Dict[str, Any]:
        """
        Parse user voice input into structured intent
        
        Args:
            user_input: User's spoken request (e.g., "Plan a 3-day trip to Jaipur...")
        
        Returns:
            Structured intent dictionary
        """
        # Use simple parser if LLM is unavailable or explicitly requested
        if self.use_simple_parser:
            return self.simple_parser.parse(user_input)
        
        prompt = f"""
        Parse the following travel planning request into structured JSON.
        
        User input: "{user_input}"
        
        Extract ALL information mentioned:
        1. city: City name (e.g., "Jaipur"). Look for patterns like "city is X", "to X", "visit X", "X trip"
        2. duration: Number of days as integer. Convert words to numbers: "three days" -> 3, "2-day" -> 2
        3. interests: List of interests (e.g., ["food", "culture"]). Extract from words like "like", "interested in", "love"
        4. pace: Travel pace ("relaxed", "moderate", "fast"). Default to "moderate" if not mentioned
        5. dates: Dates if mentioned (optional)
        6. constraints: Any other constraints mentioned (optional)
        
        Be flexible with parsing:
        - "city is Jaipur duration is three days" -> {{"city": "Jaipur", "duration": 3}}
        - "3-day trip to Jaipur" -> {{"city": "Jaipur", "duration": 3}}
        - "Plan Jaipur for 3 days" -> {{"city": "Jaipur", "duration": 3}}
        
        Return ONLY valid JSON in this exact format:
        {{
            "city": "string or null",
            "duration": integer or null,
            "interests": ["string"] or [],
            "pace": "relaxed" or "moderate" or "fast",
            "dates": null,
            "constraints": {{}},
            "missing_info": ["list of what's still missing from: city, duration, interests"]
        }}
        
        If a field is not mentioned, set it to null (or [] for interests).
        """
        
        system_prompt = "You are a travel planning assistant. Parse user requests into structured JSON format. Be precise and extract all mentioned information."
        
        try:
            result = self.llm_client.call_with_json(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3
            )
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ LLM parsing failed: {error_msg}")
            
            # Check if it's a quota error
            if "quota" in error_msg.lower() or "429" in error_msg:
                print("⚠️ API quota exceeded - falling back to simple parser")
                self.use_simple_parser = True
                return self.simple_parser.parse(user_input)
            
            # For other errors, also fall back to simple parser
            print("⚠️ Falling back to simple rule-based parser")
            return self.simple_parser.parse(user_input)


# Test function
if __name__ == "__main__":
    parser = IntentParser()
    
    test_input = "Plan a 3-day trip to Jaipur next weekend. I like food and culture, relaxed pace."
    
    print("🔍 Testing Intent Parser...")
    print(f"Input: {test_input}\n")
    
    result = parser.parse(test_input)
    
    print("✅ Parsed Intent:")
    print(f"   City: {result.get('city')}")
    print(f"   Duration: {result.get('duration')} days")
    print(f"   Interests: {result.get('interests')}")
    print(f"   Pace: {result.get('pace')}")
    print(f"   Missing info: {result.get('missing_info', [])}")
