"""
Grounding & Hallucination Evaluation
Checks:
- POIs map to dataset records (OSM IDs)
- Tips cite RAG sources
- Uncertainty is explicitly stated when data is missing
"""
import os
import sys
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GroundingEval:
    """
    Evaluation for grounding and hallucination detection
    """
    
    def __init__(self):
        # Known OSM ID patterns
        self.osm_id_patterns = ["node/", "way/", "relation/"]
    
    def run(
        self,
        itinerary: Dict,
        pois: List[Dict],
        explanations: List[Dict]
    ) -> Dict[str, Any]:
        """
        Run grounding evaluation
        
        Args:
            itinerary: The generated itinerary
            pois: List of POIs used (with IDs)
            explanations: List of explanations generated
        
        Returns:
            Evaluation results
        """
        # Check 1: POI grounding (OSM IDs)
        poi_grounding = self._check_poi_grounding(itinerary, pois)
        
        # Check 2: Explanation citations
        citation_check = self._check_citations(explanations)
        
        # Check 3: Uncertainty handling
        uncertainty_check = self._check_uncertainty_handling(explanations)
        
        # Calculate score
        score = 0.0
        score += 0.4 * (poi_grounding["grounded_ratio"])
        score += 0.4 * (citation_check["citation_ratio"])
        score += 0.2 * (1.0 if uncertainty_check["properly_handled"] else 0.5)
        
        passed = (
            poi_grounding["grounded_ratio"] >= 0.8 and
            citation_check["citation_ratio"] >= 0.5
        )
        
        return {
            "eval_name": "grounding",
            "passed": passed,
            "score": score,
            "checks": {
                "poi_grounding": poi_grounding,
                "citations": citation_check,
                "uncertainty": uncertainty_check
            }
        }
    
    def _check_poi_grounding(
        self,
        itinerary: Dict,
        pois: List[Dict]
    ) -> Dict[str, Any]:
        """Check if POIs in itinerary have valid OSM IDs"""
        # Get all POI IDs from itinerary
        itinerary_poi_ids = set()
        for day in itinerary.get("days", []):
            for block in day.get("blocks", []):
                for poi in block.get("pois", []):
                    itinerary_poi_ids.add(poi.get("poiId", ""))
        
        # Create lookup of POIs with OSM IDs
        grounded_pois = {}
        for poi in pois:
            poi_id = poi.get("id", "")
            osm_id = poi.get("osmId", poi_id)
            
            # Check if OSM ID is valid
            is_valid = any(pattern in str(osm_id) for pattern in self.osm_id_patterns)
            grounded_pois[poi.get("name", poi_id)] = {
                "osm_id": osm_id,
                "is_grounded": is_valid
            }
        
        # Count grounded POIs
        grounded_count = sum(1 for v in grounded_pois.values() if v["is_grounded"])
        total_count = len(grounded_pois) or 1
        
        return {
            "total_pois": len(itinerary_poi_ids),
            "grounded_count": grounded_count,
            "grounded_ratio": grounded_count / total_count,
            "ungrounded": [k for k, v in grounded_pois.items() if not v["is_grounded"]]
        }
    
    def _check_citations(
        self,
        explanations: List[Dict]
    ) -> Dict[str, Any]:
        """Check if explanations have citations"""
        if not explanations:
            return {
                "total_explanations": 0,
                "with_citations": 0,
                "citation_ratio": 1.0  # No explanations = no violations
            }
        
        with_citations = 0
        without_citations = []
        
        for i, exp in enumerate(explanations):
            citations = exp.get("citations", [])
            if citations and len(citations) > 0:
                with_citations += 1
            else:
                without_citations.append(i)
        
        return {
            "total_explanations": len(explanations),
            "with_citations": with_citations,
            "citation_ratio": with_citations / len(explanations),
            "without_citations": without_citations
        }
    
    def _check_uncertainty_handling(
        self,
        explanations: List[Dict]
    ) -> Dict[str, Any]:
        """Check if uncertainty is properly stated when data is missing"""
        if not explanations:
            return {
                "properly_handled": True,
                "ungrounded_without_uncertainty": []
            }
        
        issues = []
        
        for i, exp in enumerate(explanations):
            grounded = exp.get("grounded", True)
            uncertainty = exp.get("uncertainty")
            
            # If not grounded, should have uncertainty message
            if not grounded and not uncertainty:
                issues.append({
                    "index": i,
                    "issue": "Ungrounded explanation without uncertainty statement"
                })
        
        return {
            "properly_handled": len(issues) == 0,
            "ungrounded_without_uncertainty": issues
        }


# Test function
if __name__ == "__main__":
    eval = GroundingEval()
    
    # Test data
    test_itinerary = {
        "days": [
            {
                "day": 1,
                "blocks": [
                    {"type": "morning", "pois": [{"poiId": "Hawa Mahal"}]},
                    {"type": "afternoon", "pois": [{"poiId": "City Palace"}]}
                ]
            }
        ]
    }
    
    test_pois = [
        {"name": "Hawa Mahal", "id": "node/123456", "osmId": "node/123456"},
        {"name": "City Palace", "id": "way/234567", "osmId": "way/234567"}
    ]
    
    test_explanations = [
        {
            "explanation": "Hawa Mahal is famous for its unique architecture.",
            "citations": [{"source": "wikivoyage", "text": "..."}],
            "grounded": True
        },
        {
            "explanation": "City Palace is a must-see attraction.",
            "citations": [],
            "grounded": False,
            "uncertainty": "Limited information available"
        }
    ]
    
    print("🔍 Running Grounding Eval...")
    result = eval.run(test_itinerary, test_pois, test_explanations)
    
    print(f"Passed: {result['passed']}")
    print(f"Score: {result['score']:.2f}")
    print(f"POI Grounding: {result['checks']['poi_grounding']['grounded_ratio']:.0%}")
    print(f"Citations: {result['checks']['citations']['citation_ratio']:.0%}")
    print(f"Uncertainty Handled: {result['checks']['uncertainty']['properly_handled']}")
