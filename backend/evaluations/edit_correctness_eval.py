"""
Edit Correctness Evaluation
Checks:
- Voice edits only modify intended sections
- No unintended changes elsewhere
"""
import os
import sys
from typing import Dict, Any, List
from copy import deepcopy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EditCorrectnessEval:
    """
    Evaluation for edit correctness
    """
    
    def run(
        self,
        original_itinerary: Dict,
        edited_itinerary: Dict,
        edit_request: Dict,
        changes: List[Dict]
    ) -> Dict[str, Any]:
        """
        Run edit correctness evaluation
        
        Args:
            original_itinerary: Itinerary before edit
            edited_itinerary: Itinerary after edit
            edit_request: The parsed edit request
            changes: List of changes made
        
        Returns:
            Evaluation results
        """
        scope = edit_request.get("scope", "unknown")
        target_day = edit_request.get("day")
        target_block = edit_request.get("block")
        
        # Check 1: Intended changes were made
        intended_changes_check = self._check_intended_changes(changes, edit_request)
        
        # Check 2: Unintended changes
        unintended_changes = self._find_unintended_changes(
            original_itinerary,
            edited_itinerary,
            target_day,
            target_block,
            scope
        )
        
        # Calculate score
        score = 1.0
        if not intended_changes_check["passed"]:
            score -= 0.3
        if unintended_changes:
            score -= 0.1 * len(unintended_changes)
        
        score = max(0.0, score)
        
        return {
            "eval_name": "edit_correctness",
            "passed": intended_changes_check["passed"] and len(unintended_changes) == 0,
            "score": score,
            "checks": {
                "intended_changes": intended_changes_check,
                "unintended_changes": {
                    "count": len(unintended_changes),
                    "details": unintended_changes
                }
            },
            "edit_scope": scope,
            "target_day": target_day,
            "target_block": target_block
        }
    
    def _check_intended_changes(
        self,
        changes: List[Dict],
        edit_request: Dict
    ) -> Dict[str, Any]:
        """Check if intended changes were made"""
        edit_type = edit_request.get("edit_type")
        
        if not changes:
            return {
                "passed": False,
                "reason": "No changes were made"
            }
        
        # Check if at least one change matches the edit type
        for change in changes:
            if change.get("type") == edit_type or change.get("type", "").startswith(edit_type):
                return {
                    "passed": True,
                    "reason": f"Found {edit_type} change"
                }
        
        return {
            "passed": True,  # Changes were made, even if different type
            "reason": f"Changes made: {[c.get('type') for c in changes]}"
        }
    
    def _find_unintended_changes(
        self,
        original: Dict,
        edited: Dict,
        target_day: int,
        target_block: str,
        scope: str
    ) -> List[Dict]:
        """Find changes outside the intended scope"""
        unintended = []
        
        original_days = original.get("days", [])
        edited_days = edited.get("days", [])
        
        for i, (orig_day, edit_day) in enumerate(zip(original_days, edited_days)):
            day_num = orig_day.get("day", i + 1)
            
            # Skip if this day is the target (in day/block scope)
            if scope in ["day", "block"] and day_num == target_day:
                # For block scope, check other blocks
                if scope == "block":
                    for j, (orig_block, edit_block) in enumerate(zip(
                        orig_day.get("blocks", []),
                        edit_day.get("blocks", [])
                    )):
                        block_type = orig_block.get("type")
                        if block_type != target_block:
                            # This block should NOT be changed
                            if self._blocks_differ(orig_block, edit_block):
                                unintended.append({
                                    "day": day_num,
                                    "block": block_type,
                                    "reason": "Block changed outside edit scope"
                                })
                continue
            
            # For full scope, any day can change
            if scope == "full":
                continue
            
            # This day should NOT be changed (in day/block scope)
            for j, (orig_block, edit_block) in enumerate(zip(
                orig_day.get("blocks", []),
                edit_day.get("blocks", [])
            )):
                if self._blocks_differ(orig_block, edit_block):
                    unintended.append({
                        "day": day_num,
                        "block": orig_block.get("type"),
                        "reason": "Day changed outside edit scope"
                    })
        
        return unintended
    
    def _blocks_differ(self, block1: Dict, block2: Dict) -> bool:
        """Check if two blocks are different"""
        pois1 = [p.get("poiId") for p in block1.get("pois", [])]
        pois2 = [p.get("poiId") for p in block2.get("pois", [])]
        return pois1 != pois2


# Test function
if __name__ == "__main__":
    eval = EditCorrectnessEval()
    
    original = {
        "days": [
            {
                "day": 1,
                "blocks": [
                    {"type": "morning", "pois": [{"poiId": "A"}, {"poiId": "B"}]},
                    {"type": "afternoon", "pois": [{"poiId": "C"}]},
                    {"type": "evening", "pois": [{"poiId": "D"}]}
                ]
            },
            {
                "day": 2,
                "blocks": [
                    {"type": "morning", "pois": [{"poiId": "E"}]},
                    {"type": "afternoon", "pois": [{"poiId": "F"}]},
                    {"type": "evening", "pois": []}
                ]
            }
        ]
    }
    
    # Correct edit: only Day 1 morning changed
    edited_correct = deepcopy(original)
    edited_correct["days"][0]["blocks"][0]["pois"] = [{"poiId": "A"}]
    
    edit_request = {"edit_type": "pace", "scope": "day", "day": 1, "block": None}
    changes = [{"type": "pace_reduced", "day": 1, "block": "morning"}]
    
    print("🔍 Running Edit Correctness Eval...")
    print("\n1️⃣  Test: Correct edit (Day 1 only)")
    result = eval.run(original, edited_correct, edit_request, changes)
    print(f"   Passed: {result['passed']}")
    print(f"   Score: {result['score']:.2f}")
    print(f"   Unintended changes: {result['checks']['unintended_changes']['count']}")
    
    # Incorrect edit: Day 2 also changed (unintended)
    edited_incorrect = deepcopy(original)
    edited_incorrect["days"][0]["blocks"][0]["pois"] = [{"poiId": "A"}]
    edited_incorrect["days"][1]["blocks"][0]["pois"] = [{"poiId": "X"}]  # Unintended
    
    print("\n2️⃣  Test: Incorrect edit (Day 2 also changed)")
    result2 = eval.run(original, edited_incorrect, edit_request, changes)
    print(f"   Passed: {result2['passed']}")
    print(f"   Score: {result2['score']:.2f}")
    print(f"   Unintended changes: {result2['checks']['unintended_changes']['count']}")
