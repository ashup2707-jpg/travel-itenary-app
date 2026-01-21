"""
Simple rule-based intent parser (fallback when LLM quota exceeded)
"""
import re
from typing import Dict, Any, List


class SimpleIntentParser:
    """
    Rule-based intent parser that doesn't require LLM calls
    Useful as fallback when API quota is exceeded
    """
    
    def parse(self, user_input: str) -> Dict[str, Any]:
        """
        Parse user input using simple regex patterns
        
        Args:
            user_input: User's spoken/typed request
        
        Returns:
            Structured intent dictionary
        """
        user_input_lower = user_input.lower()
        
        # Extract city
        city = self._extract_city(user_input_lower)
        
        # Extract duration
        duration = self._extract_duration(user_input_lower)
        
        # Extract interests
        interests = self._extract_interests(user_input_lower)
        
        # Extract pace
        pace = self._extract_pace(user_input_lower)
        
        # Determine missing info
        missing_info = []
        if not city:
            missing_info.append("city")
        if not duration:
            missing_info.append("duration")
        if not interests:
            missing_info.append("interests")
        
        return {
            "city": city,
            "duration": duration,
            "interests": interests,
            "pace": pace,
            "dates": None,
            "constraints": {},
            "missing_info": missing_info
        }
    
    def _extract_city(self, text: str) -> str:
        """Extract city name from text"""
        # Common patterns
        patterns = [
            r'city\s+is\s+(\w+)',
            r'to\s+(\w+)',
            r'visit\s+(\w+)',
            r'trip\s+to\s+(\w+)',
            r'plan\s+(\w+)',
            r'in\s+(\w+)',
        ]
        
        # Known cities (can be expanded)
        known_cities = ['jaipur', 'delhi', 'mumbai', 'bangalore', 'goa', 'udaipur', 'agra']
        
        # Try patterns first
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                city_name = match.group(1)
                if city_name in known_cities:
                    return city_name.capitalize()
        
        # Check if any known city is mentioned
        for city in known_cities:
            if city in text:
                return city.capitalize()
        
        return None
    
    def _extract_duration(self, text: str) -> int:
        """Extract duration in days from text"""
        # Number word to digit mapping
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
        }
        
        # Patterns for duration
        patterns = [
            r'duration\s+is\s+(\w+)\s+days?',
            r'(\w+)\s*-?\s*days?',
            r'for\s+(\w+)\s+days?',
            r'(\d+)d\s+trip',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                duration_str = match.group(1)
                # Try to convert to int
                if duration_str in number_words:
                    return number_words[duration_str]
                try:
                    return int(duration_str)
                except ValueError:
                    continue
        
        # Look for standalone numbers followed by "day"
        match = re.search(r'(\d+)\s*days?', text)
        if match:
            return int(match.group(1))
        
        return None
    
    def _extract_interests(self, text: str) -> List[str]:
        """Extract interests from text"""
        interest_keywords = {
            'food': ['food', 'cuisine', 'restaurant', 'eat', 'dining'],
            'culture': ['culture', 'cultural', 'heritage', 'tradition'],
            'history': ['history', 'historical', 'ancient', 'monument'],
            'nature': ['nature', 'park', 'garden', 'wildlife', 'outdoor'],
            'adventure': ['adventure', 'trekking', 'hiking', 'sports'],
            'shopping': ['shopping', 'market', 'bazaar', 'mall'],
            'art': ['art', 'museum', 'gallery', 'painting'],
            'architecture': ['architecture', 'building', 'palace', 'fort'],
        }
        
        interests = []
        for interest, keywords in interest_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    if interest not in interests:
                        interests.append(interest)
                    break
        
        return interests
    
    def _extract_pace(self, text: str) -> str:
        """Extract travel pace from text"""
        if any(word in text for word in ['relaxed', 'slow', 'leisurely', 'easy']):
            return 'relaxed'
        elif any(word in text for word in ['fast', 'quick', 'packed', 'busy']):
            return 'fast'
        else:
            return 'moderate'


# Test
if __name__ == "__main__":
    parser = SimpleIntentParser()
    
    test_inputs = [
        "Lenovo 3D trip to Jaipur",
        "city is Jaipur duration is three days",
        "Plan a 3-day trip to Jaipur. I like food and culture.",
        "3 days in Jaipur",
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        result = parser.parse(test_input)
        print(f"  City: {result['city']}")
        print(f"  Duration: {result['duration']}")
        print(f"  Interests: {result['interests']}")
        print(f"  Pace: {result['pace']}")
        print(f"  Missing: {result['missing_info']}")
