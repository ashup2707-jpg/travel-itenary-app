"""
Feasibility Evaluation
Checks:
- Daily duration ≤ available time
- Reasonable travel times
- Pace consistency
"""
import os
import sys
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from symbolic.feasibility_engine import FeasibilityEngine

class FeasibilityEval:
    """
    Evaluation for itinerary feasibility
    """
    
    def __init__(self):
        self.engine = FeasibilityEngine()
    
    def run(
        self,
        itinerary: Dict,
        constraints: Dict
    ) -> Dict[str, Any]:
        """
        Run feasibility evaluation
        
        Args:
            itinerary: The generated itinerary
            constraints: Original constraints
        
        Returns:
            Evaluation results
        """
        # Run feasibility engine
        result = self.engine.evaluate(itinerary, constraints)
        
        # Format as evaluation result
        return {
            "eval_name": "feasibility",
            "passed": result["is_feasible"],
            "score": result["overall_score"],
            "checks": {
                "duration": self._count_passed(result["checks"], "daily_duration"),
                "travel_time": self._count_passed(result["checks"], "travel_time"),
                "pace": self._count_passed(result["checks"], "pace_consistency")
            },
            "errors": result["errors"],
            "warnings": result["warnings"],
            "details": result["checks"]
        }
    
    def _count_passed(self, checks: List[Dict], check_type: str) -> Dict[str, int]:
        """Count passed/failed for a check type"""
        type_checks = [c for c in checks if c["check"] == check_type]
        passed = sum(1 for c in type_checks if c["passed"])
        return {
            "total": len(type_checks),
            "passed": passed,
            "failed": len(type_checks) - passed
        }


# Test function
if __name__ == "__main__":
    eval = FeasibilityEval()
    
    test_itinerary = {
        "days": [
            {
                "day": 1,
                "totalTravelTime": 60,
                "blocks": [
                    {"type": "morning", "totalDuration": 180, "pois": [{"poiId": "A"}, {"poiId": "B"}]},
                    {"type": "afternoon", "totalDuration": 240, "pois": [{"poiId": "C"}]},
                    {"type": "evening", "totalDuration": 120, "pois": [{"poiId": "D"}]}
                ]
            }
        ]
    }
    
    constraints = {"pace": "moderate"}
    
    print("🔍 Running Feasibility Eval...")
    result = eval.run(test_itinerary, constraints)
    
    print(f"Passed: {result['passed']}")
    print(f"Score: {result['score']:.2f}")
    print(f"Checks: {result['checks']}")
    print(f"Errors: {result['errors']}")
    print(f"Warnings: {result['warnings']}")
