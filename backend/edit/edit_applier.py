"""
Edit Applier - Applies edits to itinerary (partial regeneration)
Only modifies affected parts, preserves rest
"""
import os
import sys
from typing import Dict, Any, List, Optional
from copy import deepcopy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_tools.poi_search.implementation import POISearchMCP
from mcp_tools.poi_search.schema import POISearchInput

class EditApplier:
    """
    Applies edits to itinerary with minimal changes
    Only regenerates affected parts
    """
    
    def __init__(self, use_mock_data: bool = False):
        self.poi_search = POISearchMCP(use_mock=use_mock_data)
    
    def apply(
        self,
        itinerary: Dict,
        edit_request: Dict,
        constraints: Dict
    ) -> Dict[str, Any]:
        """
        Apply edit to itinerary
        
        Args:
            itinerary: Current itinerary
            edit_request: Parsed edit request
            constraints: Original constraints (city, interests, etc.)
        
        Returns:
            Updated itinerary with diff info
        """
        # Make a copy to avoid mutating original
        updated_itinerary = deepcopy(itinerary)
        
        edit_type = edit_request.get("edit_type")
        scope = edit_request.get("scope")
        day = edit_request.get("day")
        block = edit_request.get("block")
        value = edit_request.get("value")
        category = edit_request.get("category")
        
        changes = []
        
        if edit_type == "pace":
            changes = self._apply_pace_edit(updated_itinerary, day, value)
        
        elif edit_type == "swap":
            changes = self._apply_swap_edit(updated_itinerary, day, block, value, category, constraints)
        
        elif edit_type == "add":
            changes = self._apply_add_edit(updated_itinerary, day, block, category, constraints)
        
        elif edit_type == "remove":
            changes = self._apply_remove_edit(updated_itinerary, day, block, value)
        
        elif edit_type == "reduce_travel":
            changes = self._apply_reduce_travel_edit(updated_itinerary, day)
        
        elif edit_type == "replace":
            changes = self._apply_swap_edit(updated_itinerary, day, block, value, category, constraints)
        
        else:
            return {
                "success": False,
                "error": f"Unknown edit type: {edit_type}",
                "itinerary": itinerary,
                "changes": []
            }
        
        return {
            "success": True,
            "itinerary": updated_itinerary,
            "changes": changes,
            "edit_type": edit_type,
            "scope": scope
        }
    
    def _apply_pace_edit(
        self,
        itinerary: Dict,
        day: Optional[int],
        pace: str
    ) -> List[Dict]:
        """Apply pace change - reduce or increase POIs per block"""
        changes = []
        
        # Determine target days
        if day:
            target_days = [d for d in itinerary["days"] if d["day"] == day]
        else:
            target_days = itinerary["days"]
        
        for d in target_days:
            for block in d.get("blocks", []):
                original_count = len(block.get("pois", []))
                
                if pace == "relaxed" and original_count > 1:
                    # Remove extra POIs for relaxed pace
                    block["pois"] = block["pois"][:1]
                    changes.append({
                        "type": "pace_reduced",
                        "day": d["day"],
                        "block": block["type"],
                        "from_count": original_count,
                        "to_count": 1
                    })
                elif pace == "fast" and original_count < 2:
                    # Would need to add POIs - mark for future
                    changes.append({
                        "type": "pace_note",
                        "day": d["day"],
                        "block": block["type"],
                        "note": "Would add more POIs for fast pace"
                    })
        
        return changes
    
    def _apply_swap_edit(
        self,
        itinerary: Dict,
        day: Optional[int],
        block_type: Optional[str],
        value: Optional[str],
        category: Optional[str],
        constraints: Dict
    ) -> List[Dict]:
        """Swap POIs in specified block"""
        changes = []
        
        # Find target block
        for d in itinerary["days"]:
            if day and d["day"] != day:
                continue
            
            for block in d.get("blocks", []):
                if block_type and block["type"] != block_type:
                    continue
                
                # Search for replacement POI
                search_interests = [category] if category else constraints.get("interests", [])
                if value:
                    search_interests.append(value)
                
                try:
                    poi_input = POISearchInput(
                        city=constraints.get("city", "Jaipur"),
                        interests=search_interests,
                        constraints={"indoor": value == "indoors"} if value == "indoors" else {}
                    )
                    
                    poi_results = self.poi_search.search(poi_input)
                    
                    if poi_results.pois:
                        # Find a POI not already in itinerary
                        existing_poi_ids = self._get_all_poi_ids(itinerary)
                        new_poi = None
                        
                        for poi in poi_results.pois:
                            if poi.id not in existing_poi_ids:
                                new_poi = poi
                                break
                        
                        if new_poi and block.get("pois"):
                            old_poi = block["pois"][0]["poiId"]
                            block["pois"][0]["poiId"] = new_poi.id
                            changes.append({
                                "type": "swap",
                                "day": d["day"],
                                "block": block["type"],
                                "old_poi": old_poi,
                                "new_poi": new_poi.id,
                                "reason": f"Swapped for {value or category or 'alternative'}"
                            })
                except Exception as e:
                    changes.append({
                        "type": "swap_error",
                        "day": d["day"],
                        "block": block["type"],
                        "error": str(e)
                    })
        
        return changes
    
    def _apply_add_edit(
        self,
        itinerary: Dict,
        day: Optional[int],
        block_type: Optional[str],
        category: Optional[str],
        constraints: Dict
    ) -> List[Dict]:
        """Add a POI to the itinerary"""
        changes = []
        
        # Search for POI to add
        search_interests = [category] if category else constraints.get("interests", [])
        
        try:
            poi_input = POISearchInput(
                city=constraints.get("city", "Jaipur"),
                interests=search_interests,
                constraints={}
            )
            
            poi_results = self.poi_search.search(poi_input)
            
            if poi_results.pois:
                # Find a POI not already in itinerary
                existing_poi_ids = self._get_all_poi_ids(itinerary)
                new_poi = None
                
                for poi in poi_results.pois:
                    if poi.id not in existing_poi_ids:
                        new_poi = poi
                        break
                
                if new_poi:
                    # Find best day/block to add
                    target_day = day or 1
                    target_block = block_type or "afternoon"
                    
                    for d in itinerary["days"]:
                        if d["day"] == target_day:
                            for block in d.get("blocks", []):
                                if block["type"] == target_block:
                                    block["pois"].append({
                                        "poiId": new_poi.id,
                                        "duration": new_poi.estimatedDuration
                                    })
                                    changes.append({
                                        "type": "add",
                                        "day": target_day,
                                        "block": target_block,
                                        "poi": new_poi.id,
                                        "category": category
                                    })
                                    break
                            break
        except Exception as e:
            changes.append({
                "type": "add_error",
                "error": str(e)
            })
        
        return changes
    
    def _apply_remove_edit(
        self,
        itinerary: Dict,
        day: Optional[int],
        block_type: Optional[str],
        poi_name: Optional[str]
    ) -> List[Dict]:
        """Remove a POI from the itinerary"""
        changes = []
        
        for d in itinerary["days"]:
            if day and d["day"] != day:
                continue
            
            for block in d.get("blocks", []):
                if block_type and block["type"] != block_type:
                    continue
                
                # Remove POI
                original_pois = block.get("pois", [])
                if poi_name:
                    # Remove specific POI
                    block["pois"] = [p for p in original_pois if poi_name.lower() not in p.get("poiId", "").lower()]
                elif original_pois:
                    # Remove last POI
                    removed = original_pois.pop()
                    changes.append({
                        "type": "remove",
                        "day": d["day"],
                        "block": block["type"],
                        "poi": removed.get("poiId")
                    })
        
        return changes
    
    def _apply_reduce_travel_edit(
        self,
        itinerary: Dict,
        day: Optional[int]
    ) -> List[Dict]:
        """Reduce travel time by reordering or removing distant POIs"""
        changes = []
        
        # Simple implementation: reduce POIs per block
        for d in itinerary["days"]:
            if day and d["day"] != day:
                continue
            
            total_reduced = 0
            for block in d.get("blocks", []):
                if len(block.get("pois", [])) > 1:
                    # Keep only first POI to reduce travel
                    removed = len(block["pois"]) - 1
                    block["pois"] = block["pois"][:1]
                    total_reduced += removed
            
            if total_reduced > 0:
                changes.append({
                    "type": "reduce_travel",
                    "day": d["day"],
                    "pois_removed": total_reduced,
                    "note": "Reduced POIs to minimize travel"
                })
        
        return changes
    
    def _get_all_poi_ids(self, itinerary: Dict) -> List[str]:
        """Get all POI IDs currently in itinerary"""
        poi_ids = []
        for d in itinerary.get("days", []):
            for block in d.get("blocks", []):
                for poi in block.get("pois", []):
                    poi_ids.append(poi.get("poiId", ""))
        return poi_ids


# Test function
if __name__ == "__main__":
    applier = EditApplier(use_mock_data=True)
    
    # Test itinerary
    test_itinerary = {
        "days": [
            {
                "day": 1,
                "blocks": [
                    {"type": "morning", "pois": [{"poiId": "Hawa Mahal", "duration": 60}, {"poiId": "City Palace", "duration": 120}]},
                    {"type": "afternoon", "pois": [{"poiId": "Amber Fort", "duration": 180}]},
                    {"type": "evening", "pois": [{"poiId": "Jantar Mantar", "duration": 60}]}
                ]
            },
            {
                "day": 2,
                "blocks": [
                    {"type": "morning", "pois": [{"poiId": "Nahargarh Fort", "duration": 180}]},
                    {"type": "afternoon", "pois": [{"poiId": "Jal Mahal", "duration": 60}]},
                    {"type": "evening", "pois": []}
                ]
            }
        ]
    }
    
    constraints = {"city": "Jaipur, India", "interests": ["culture", "history"]}
    
    print("🔧 Testing Edit Applier...")
    print("=" * 50)
    
    # Test 1: Pace edit
    print("\n1️⃣  Test: Make Day 1 more relaxed")
    edit1 = {"edit_type": "pace", "scope": "day", "day": 1, "value": "relaxed"}
    result1 = applier.apply(test_itinerary, edit1, constraints)
    print(f"   Success: {result1['success']}")
    print(f"   Changes: {result1['changes']}")
    
    # Test 2: Reduce travel
    print("\n2️⃣  Test: Reduce travel time")
    edit2 = {"edit_type": "reduce_travel", "scope": "full", "day": None}
    result2 = applier.apply(test_itinerary, edit2, constraints)
    print(f"   Success: {result2['success']}")
    print(f"   Changes: {result2['changes']}")
    
    print("\n" + "=" * 50)
    print("✅ Edit Applier test complete!")
