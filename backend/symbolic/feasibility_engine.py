"""
Feasibility Engine - Symbolic validation of itineraries
Checks:
- Daily duration ≤ available time
- Reasonable travel times
- Pace consistency
"""
from typing import Dict, Any, List

class FeasibilityEngine:
    """
    Symbolic feasibility validation engine
    """
    
    def __init__(self):
        # Default constraints
        self.default_available_time = 12 * 60  # 12 hours per day (9am-9pm)
        self.max_travel_time_ratio = 0.4  # Max 40% of time traveling
        self.pace_poi_limits = {
            "relaxed": {"min": 1, "max": 3},  # 1-3 POIs per day
            "moderate": {"min": 2, "max": 5},  # 2-5 POIs per day
            "fast": {"min": 4, "max": 8}  # 4-8 POIs per day
        }
    
    def evaluate(
        self,
        itinerary: Dict,
        constraints: Dict
    ) -> Dict[str, Any]:
        """
        Evaluate itinerary feasibility
        
        Args:
            itinerary: The generated itinerary
            constraints: Original constraints (pace, etc.)
        
        Returns:
            Feasibility report with score and issues
        """
        results = {
            "overall_score": 1.0,
            "is_feasible": True,
            "checks": [],
            "warnings": [],
            "errors": []
        }
        
        pace = constraints.get("pace", "moderate")
        
        for day in itinerary.get("days", []):
            day_num = day.get("day", 0)
            
            # Check 1: Daily duration
            duration_check = self._check_daily_duration(day)
            results["checks"].append(duration_check)
            if not duration_check["passed"]:
                results["errors"].append(f"Day {day_num}: {duration_check['issue']}")
                results["overall_score"] -= 0.2
            
            # Check 2: Travel time ratio
            travel_check = self._check_travel_time(day)
            results["checks"].append(travel_check)
            if not travel_check["passed"]:
                if travel_check["severity"] == "warning":
                    results["warnings"].append(f"Day {day_num}: {travel_check['issue']}")
                    results["overall_score"] -= 0.1
                else:
                    results["errors"].append(f"Day {day_num}: {travel_check['issue']}")
                    results["overall_score"] -= 0.2
            
            # Check 3: Pace consistency
            pace_check = self._check_pace_consistency(day, pace)
            results["checks"].append(pace_check)
            if not pace_check["passed"]:
                results["warnings"].append(f"Day {day_num}: {pace_check['issue']}")
                results["overall_score"] -= 0.1
        
        # Clamp score
        results["overall_score"] = max(0.0, min(1.0, results["overall_score"]))
        results["is_feasible"] = results["overall_score"] >= 0.6 and len(results["errors"]) == 0
        
        return results
    
    def _check_daily_duration(self, day: Dict) -> Dict[str, Any]:
        """Check if daily duration is within available time"""
        total_duration = 0
        
        for block in day.get("blocks", []):
            total_duration += block.get("totalDuration", 0)
        
        passed = total_duration <= self.default_available_time
        
        return {
            "check": "daily_duration",
            "day": day.get("day"),
            "passed": passed,
            "value": total_duration,
            "limit": self.default_available_time,
            "issue": f"Total duration ({total_duration} min) exceeds available time ({self.default_available_time} min)" if not passed else None,
            "severity": "error" if not passed else None
        }
    
    def _check_travel_time(self, day: Dict) -> Dict[str, Any]:
        """Check if travel time is reasonable"""
        total_travel = day.get("totalTravelTime", 0)
        total_duration = 0
        
        for block in day.get("blocks", []):
            total_duration += block.get("totalDuration", 0)
        
        if total_duration == 0:
            return {
                "check": "travel_time",
                "day": day.get("day"),
                "passed": True,
                "value": 0,
                "ratio": 0,
                "issue": None,
                "severity": None
            }
        
        travel_ratio = total_travel / total_duration if total_duration > 0 else 0
        
        if travel_ratio > 0.5:
            return {
                "check": "travel_time",
                "day": day.get("day"),
                "passed": False,
                "value": total_travel,
                "ratio": travel_ratio,
                "issue": f"Travel time ({total_travel} min, {travel_ratio:.0%}) is very high",
                "severity": "error"
            }
        elif travel_ratio > self.max_travel_time_ratio:
            return {
                "check": "travel_time",
                "day": day.get("day"),
                "passed": False,
                "value": total_travel,
                "ratio": travel_ratio,
                "issue": f"Travel time ({total_travel} min, {travel_ratio:.0%}) exceeds recommended {self.max_travel_time_ratio:.0%}",
                "severity": "warning"
            }
        
        return {
            "check": "travel_time",
            "day": day.get("day"),
            "passed": True,
            "value": total_travel,
            "ratio": travel_ratio,
            "issue": None,
            "severity": None
        }
    
    def _check_pace_consistency(self, day: Dict, pace: str) -> Dict[str, Any]:
        """Check if POI count matches pace"""
        poi_count = 0
        
        for block in day.get("blocks", []):
            poi_count += len(block.get("pois", []))
        
        limits = self.pace_poi_limits.get(pace, self.pace_poi_limits["moderate"])
        
        if poi_count < limits["min"]:
            return {
                "check": "pace_consistency",
                "day": day.get("day"),
                "passed": False,
                "value": poi_count,
                "expected_min": limits["min"],
                "expected_max": limits["max"],
                "pace": pace,
                "issue": f"Too few POIs ({poi_count}) for {pace} pace (min: {limits['min']})",
                "severity": "warning"
            }
        elif poi_count > limits["max"]:
            return {
                "check": "pace_consistency",
                "day": day.get("day"),
                "passed": False,
                "value": poi_count,
                "expected_min": limits["min"],
                "expected_max": limits["max"],
                "pace": pace,
                "issue": f"Too many POIs ({poi_count}) for {pace} pace (max: {limits['max']})",
                "severity": "warning"
            }
        
        return {
            "check": "pace_consistency",
            "day": day.get("day"),
            "passed": True,
            "value": poi_count,
            "expected_min": limits["min"],
            "expected_max": limits["max"],
            "pace": pace,
            "issue": None,
            "severity": None
        }


# Test function
if __name__ == "__main__":
    engine = FeasibilityEngine()
    
    # Test itinerary
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
            },
            {
                "day": 2,
                "totalTravelTime": 180,  # High travel time
                "blocks": [
                    {"type": "morning", "totalDuration": 180, "pois": [{"poiId": "E"}]},
                    {"type": "afternoon", "totalDuration": 240, "pois": [{"poiId": "F"}]},
                    {"type": "evening", "totalDuration": 60, "pois": []}
                ]
            }
        ]
    }
    
    constraints = {"pace": "moderate"}
    
    print("🔍 Testing Feasibility Engine...")
    print("=" * 50)
    
    result = engine.evaluate(test_itinerary, constraints)
    
    print(f"Overall Score: {result['overall_score']:.2f}")
    print(f"Is Feasible: {result['is_feasible']}")
    print(f"Errors: {result['errors']}")
    print(f"Warnings: {result['warnings']}")
    
    print("\nChecks:")
    for check in result["checks"]:
        status = "✅" if check["passed"] else "❌"
        print(f"  {status} Day {check['day']} - {check['check']}: {check.get('issue', 'OK')}")
    
    print("\n" + "=" * 50)
    print("✅ Feasibility Engine test complete!")
