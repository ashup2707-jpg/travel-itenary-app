"""
POI Search MCP Implementation
Searches OpenStreetMap for Points of Interest
"""
import sys
import os
import random
from datetime import datetime
from typing import List, Dict

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data_sources.osm_client import OSMClient
from mcp_tools.poi_search.schema import POISearchInput, POISearchOutput, POI

class POISearchMCP:
    """
    POI Search MCP Tool
    Searches OpenStreetMap for Points of Interest based on city, interests, and constraints
    """
    
    def __init__(self, use_mock: bool = False):
        """
        Initialize POI Search MCP
        
        Args:
            use_mock: If True, use mock data instead of real API (for testing)
        """
        self.osm_client = OSMClient(use_mock=use_mock)
    
    def search(
        self,
        input_data: POISearchInput
    ) -> POISearchOutput:
        """
        Search for POIs
        
        Args:
            input_data: POISearchInput with city, interests, constraints
        
        Returns:
            POISearchOutput with ranked POIs
        """
        city = input_data.city
        interests = input_data.interests
        constraints = input_data.constraints
        
        # Map interests to OSM categories
        category_mapping = {
            'food': ['amenity'],
            'culture': ['tourism', 'historic'],
            'history': ['historic', 'tourism'],
            'shopping': ['shop', 'amenity'],
            'nature': ['leisure', 'natural'],
            'religion': ['amenity'],
            'architecture': ['historic', 'tourism'],
            'entertainment': ['leisure', 'amenity'],
            'sports': ['leisure', 'sport'],
            'art': ['tourism', 'amenity']
        }
        
        # Get categories to search
        categories_to_search = []
        for interest in interests:
            if interest.lower() in category_mapping:
                categories_to_search.extend(category_mapping[interest.lower()])
        
        # Remove duplicates
        categories_to_search = list(set(categories_to_search))
        
        if not categories_to_search:
            # Default categories if no mapping found
            categories_to_search = ['tourism', 'amenity', 'historic']
        
        # Search OSM
        pois_raw = self.osm_client.search_pois(
            city=city,
            categories=categories_to_search,
            limit=50
        )
        
        # Filter by constraints (fall back to unfiltered only if constraints remove everything)
        filtered_pois = self._apply_constraints(pois_raw, constraints)
        if not filtered_pois and pois_raw:
            filtered_pois = pois_raw
        
        # Rank POIs (prefer known names for better RAG match, then shuffle for variety)
        ranked_pois = self._rank_pois(filtered_pois, interests, city)
        
        # Convert to POI schema
        pois = []
        for poi_data in ranked_pois[:40]:  # Return more POIs for variety
            poi = POI(
                id=poi_data['id'],
                name=poi_data['name'],
                category=poi_data['category'],
                coordinates=poi_data['coordinates'],
                estimatedDuration=self._estimate_duration(poi_data),
                openingHours=poi_data.get('tags', {}).get('opening_hours'),
                source='osm',
                metadata={
                    'subcategory': poi_data.get('subcategory', ''),
                    'tags': poi_data.get('tags', {})
                }
            )
            pois.append(poi)
        
        return POISearchOutput(
            pois=pois,
            totalFound=len(ranked_pois),
            queryTime=datetime.now().isoformat()
        )
    
    def _apply_constraints(self, pois: List[Dict], constraints: Dict) -> List[Dict]:
        """Apply constraints to filter POIs"""
        filtered = pois
        
        # Filter by indoor/outdoor
        if constraints.get('indoorOnly'):
            # This is a simple heuristic - in real implementation, would check tags
            filtered = [p for p in filtered if 'indoor' in str(p.get('tags', {})).lower()]
        
        # Filter by accessibility (if specified)
        if constraints.get('accessibility'):
            # Check for wheelchair accessible tags
            filtered = [p for p in filtered if 'wheelchair' in str(p.get('tags', {})).lower()]
        
        return filtered
    
    # Well-known POI names (curated/RAG) to rank higher when present
    _PREFERRED_NAMES = frozenset({
        "amer fort", "amber fort", "hawa mahal", "city palace", "nahargarh fort",
        "jaigarh fort", "jal mahal", "jantar mantar", "albert hall museum",
        "birla mandir", "galtaji temple", "johari bazaar", "bapu bazaar",
        "chokhi dhani", "rambagh palace", "sisodia rani garden", "central park",
        "ram niwas garden", "tripolia bazaar", "govind dev ji temple"
    })
    
    def _rank_pois(self, pois: List[Dict], interests: List[str], city: str = "") -> List[Dict]:
        """Rank: prefer known POI names (better RAG match), then shuffle for variety."""
        preferred = []
        rest = []
        for p in pois:
            name = (p.get("name") or "").strip().lower()
            if name in self._PREFERRED_NAMES:
                preferred.append(p)
            else:
                rest.append(p)
        random.shuffle(preferred)
        random.shuffle(rest)
        return preferred + rest
    
    def _estimate_duration(self, poi_data: Dict) -> int:
        """Estimate visit duration in minutes"""
        category = poi_data.get('category', '')
        subcategory = poi_data.get('subcategory', '')
        
        # Duration estimates based on category
        duration_map = {
            'palace': 120,
            'fort': 180,
            'museum': 90,
            'temple': 60,
            'market': 120,
            'park': 60,
            'monument': 45,
            'restaurant': 90,
            'cafe': 30
        }
        
        for key, duration in duration_map.items():
            if key in subcategory.lower() or key in str(poi_data.get('tags', {})).lower():
                return duration
        
        # Default duration
        return 60


# Test function
if __name__ == "__main__":
    import sys
    
    # Allow mock mode for testing
    use_mock = "--mock" in sys.argv or "-m" in sys.argv
    
    if use_mock:
        print("🧪 Using MOCK mode (no API calls)")
    
    mcp = POISearchMCP(use_mock=use_mock)
    
    # Test input
    test_input = POISearchInput(
        city="Jaipur, India",
        interests=["culture", "history"],
        constraints={}
    )
    
    print("🔍 Testing POI Search MCP...")
    result = mcp.search(test_input)
    
    print(f"\n✅ Found {result.totalFound} POIs")
    print(f"📋 Returning top {len(result.pois)} POIs\n")
    
    for poi in result.pois[:5]:
        print(f"📍 {poi.name}")
        print(f"   ID: {poi.id}")
        print(f"   Category: {poi.category}")
        print(f"   Duration: {poi.estimatedDuration} minutes")
        print()
