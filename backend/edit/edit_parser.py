"""
Edit Parser - Parses voice edit commands into structured edit requests
"""
import os
import sys
from typing import Dict, Any, Optional, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.llm_client import LLMClient

class EditParser:
    """
    Parses voice edit commands into structured edit requests
    Examples:
    - "Make Day 2 more relaxed" → EditRequest(day=2, edit_type="pace", value="relaxed")
    - "Swap the Day 1 evening plan" → EditRequest(day=1, block="evening", edit_type="swap")
    - "Add a food place on Day 3" → EditRequest(day=3, edit_type="add", category="food")
    """
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def parse(self, edit_command: str, current_itinerary: Dict) -> Dict[str, Any]:
        """
        Parse edit command into structured edit request
        
        Args:
            edit_command: User's edit command (voice input)
            current_itinerary: Current itinerary to understand context
        
        Returns:
            Structured edit request
        """
        # Get number of days from itinerary
        num_days = len(current_itinerary.get("days", []))
        
        prompt = f"""
        Parse this travel itinerary edit command into structured JSON.
        
        Edit command: "{edit_command}"
        
        Current itinerary has {num_days} days.
        
        Extract:
        1. edit_type: One of "pace", "swap", "add", "remove", "replace", "reduce_travel", "weather"
        2. scope: What part to edit - "day", "block", "poi", or "full"
        3. day: Day number (1, 2, 3, etc.) or null if affects all days
        4. block: Block type ("morning", "afternoon", "evening") or null
        5. value: The new value or requirement (e.g., "relaxed", "indoors", specific POI name)
        6. category: Category filter if adding/replacing (e.g., "food", "culture", "history")
        
        Return JSON:
        {{
            "edit_type": "pace|swap|add|remove|replace|reduce_travel|weather",
            "scope": "day|block|poi|full",
            "day": number or null,
            "block": "morning|afternoon|evening" or null,
            "value": "string" or null,
            "category": "string" or null,
            "understood": true/false,
            "clarification_needed": "string or null"
        }}
        
        Examples:
        - "Make Day 2 more relaxed" → {{"edit_type": "pace", "scope": "day", "day": 2, "block": null, "value": "relaxed", "category": null, "understood": true}}
        - "Swap the Day 1 evening plan to something indoors" → {{"edit_type": "swap", "scope": "block", "day": 1, "block": "evening", "value": "indoors", "category": null, "understood": true}}
        - "Add one famous local food place" → {{"edit_type": "add", "scope": "full", "day": null, "block": null, "value": "famous local", "category": "food", "understood": true}}
        - "Reduce travel time" → {{"edit_type": "reduce_travel", "scope": "full", "day": null, "block": null, "value": null, "category": null, "understood": true}}
        """
        
        try:
            result = self.llm_client.call_with_json(
                prompt=prompt,
                temperature=0.2
            )
            return result
        except Exception as e:
            return {
                "edit_type": "unknown",
                "scope": "unknown",
                "day": None,
                "block": None,
                "value": None,
                "category": None,
                "understood": False,
                "clarification_needed": f"Could not understand edit: {str(e)}"
            }


# Test function
if __name__ == "__main__":
    parser = EditParser()
    
    test_commands = [
        "Make Day 2 more relaxed",
        "Swap the Day 1 evening plan to something indoors",
        "Reduce travel time",
        "Add one famous local food place"
    ]
    
    test_itinerary = {"days": [{"day": 1}, {"day": 2}, {"day": 3}]}
    
    print("🔍 Testing Edit Parser...")
    print("=" * 50)
    
    for cmd in test_commands:
        print(f"\nCommand: \"{cmd}\"")
        result = parser.parse(cmd, test_itinerary)
        print(f"  Type: {result.get('edit_type')}")
        print(f"  Scope: {result.get('scope')}")
        print(f"  Day: {result.get('day')}")
        print(f"  Block: {result.get('block')}")
        print(f"  Value: {result.get('value')}")
        print(f"  Understood: {result.get('understood')}")
    
    print("\n" + "=" * 50)
    print("✅ Edit Parser test complete!")
