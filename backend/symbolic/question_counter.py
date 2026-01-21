"""
Question Counter - Symbolic validation for max 6 questions
"""
from typing import Optional

class QuestionCounter:
    """
    Tracks question count and enforces max 6 questions limit
    """
    
    def __init__(self, max_questions: int = 6):
        self.max_questions = max_questions
        self.count = 0
    
    def increment(self):
        """Increment question count"""
        self.count += 1
    
    def get_count(self) -> int:
        """Get current question count"""
        return self.count
    
    def is_max_reached(self) -> bool:
        """Check if max questions reached"""
        return self.count >= self.max_questions
    
    def reset(self):
        """Reset counter (for new conversation)"""
        self.count = 0
