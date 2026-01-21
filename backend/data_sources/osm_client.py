"""
OpenStreetMap Overpass API client for POI queries
"""
import requests
import overpy
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

class OSMClient:
    """
    Client for querying OpenStreetMap data via Overpass API
    """
    
    def __init__(self, use_mock: bool = False):
        """
        Initialize OSM Client
        
        Args:
            use_mock: If True, use mock data instead of real API (for testing)
        """
        self.use_mock = use_mock
        # Try different Overpass instances (fallback if one is down)
        self.overpass_instances = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://overpass.openstreetmap.ru/api/interpreter"
        ]
        self.current_instance = 0
        self.api = overpy.Overpass(url=self.overpass_instances[self.current_instance])
        self.base_url = self.overpass_instances[self.current_instance]
        # Nominatim requires User-Agent
        self.headers = {
            'User-Agent': 'TravelPlanner/1.0 (Educational Capstone Project)'
        }
    
    def get_city_bbox(self, city: str) -> Optional[Dict]:
        """
        Get bounding box for a city using Nominatim (OpenStreetMap geocoding)
        
        Args:
            city: City name (e.g., "Jaipur, India")
        
        Returns:
            Bounding box dict with {min_lat, min_lon, max_lat, max_lon} or None
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": city,
                "format": "json",
                "limit": 1
            }
            # Nominatim requires a User-Agent header
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                bbox = data[0].get("boundingbox", [])
                if bbox:
                    return {
                        "min_lat": float(bbox[0]),
                        "min_lon": float(bbox[1]),
                        "max_lat": float(bbox[2]),
                        "max_lon": float(bbox[3])
                    }
        except Exception as e:
            print(f"Error getting bbox for {city}: {e}")
        return None
    
    def _get_mock_pois(self, city: str) -> List[Dict]:
        """Return mock POI data for testing when API is unavailable"""
        # Expanded Jaipur POIs for testing
        mock_pois = [
            {
                "id": "node/123456",
                "name": "Hawa Mahal",
                "category": "tourism",
                "subcategory": "attraction",
                "coordinates": {"lat": 26.9239, "lon": 75.8267},
                "tags": {"tourism": "attraction", "name": "Hawa Mahal"},
                "source": "osm"
            },
            {
                "id": "way/234567",
                "name": "City Palace",
                "category": "tourism",
                "subcategory": "palace",
                "coordinates": {"lat": 26.9258, "lon": 75.8236},
                "tags": {"tourism": "palace", "name": "City Palace"},
                "source": "osm"
            },
            {
                "id": "node/345678",
                "name": "Amber Fort",
                "category": "historic",
                "subcategory": "fort",
                "coordinates": {"lat": 26.9855, "lon": 75.8513},
                "tags": {"historic": "fort", "name": "Amber Fort"},
                "source": "osm"
            },
            {
                "id": "node/456789",
                "name": "Jantar Mantar",
                "category": "tourism",
                "subcategory": "attraction",
                "coordinates": {"lat": 26.9247, "lon": 75.8246},
                "tags": {"tourism": "attraction", "name": "Jantar Mantar"},
                "source": "osm"
            },
            {
                "id": "way/567890",
                "name": "Nahargarh Fort",
                "category": "historic",
                "subcategory": "fort",
                "coordinates": {"lat": 26.9364, "lon": 75.8153},
                "tags": {"historic": "fort", "name": "Nahargarh Fort"},
                "source": "osm"
            },
            {
                "id": "node/678901",
                "name": "Jaigarh Fort",
                "category": "historic",
                "subcategory": "fort",
                "coordinates": {"lat": 26.9850, "lon": 75.8516},
                "tags": {"historic": "fort", "name": "Jaigarh Fort"},
                "source": "osm"
            },
            {
                "id": "way/789012",
                "name": "Albert Hall Museum",
                "category": "tourism",
                "subcategory": "museum",
                "coordinates": {"lat": 26.9124, "lon": 75.8185},
                "tags": {"tourism": "museum", "name": "Albert Hall Museum"},
                "source": "osm"
            },
            {
                "id": "node/890123",
                "name": "Jal Mahal",
                "category": "tourism",
                "subcategory": "attraction",
                "coordinates": {"lat": 26.9534, "lon": 75.8462},
                "tags": {"tourism": "attraction", "name": "Jal Mahal"},
                "source": "osm"
            },
            {
                "id": "way/901234",
                "name": "Birla Mandir",
                "category": "amenity",
                "subcategory": "place_of_worship",
                "coordinates": {"lat": 26.8983, "lon": 75.8067},
                "tags": {"amenity": "place_of_worship", "name": "Birla Mandir"},
                "source": "osm"
            },
            {
                "id": "node/012345",
                "name": "Galtaji Temple",
                "category": "amenity",
                "subcategory": "place_of_worship",
                "coordinates": {"lat": 26.9253, "lon": 75.8671},
                "tags": {"amenity": "place_of_worship", "name": "Galtaji Temple"},
                "source": "osm"
            },
            {
                "id": "way/112233",
                "name": "Johari Bazaar",
                "category": "tourism",
                "subcategory": "attraction",
                "coordinates": {"lat": 26.9196, "lon": 75.8242},
                "tags": {"tourism": "attraction", "name": "Johari Bazaar"},
                "source": "osm"
            },
            {
                "id": "node/223344",
                "name": "Bapu Bazaar",
                "category": "tourism",
                "subcategory": "attraction",
                "coordinates": {"lat": 26.9221, "lon": 75.8194},
                "tags": {"tourism": "attraction", "name": "Bapu Bazaar"},
                "source": "osm"
            },
            {
                "id": "way/334455",
                "name": "Rambagh Palace",
                "category": "tourism",
                "subcategory": "hotel",
                "coordinates": {"lat": 26.8879, "lon": 75.8108},
                "tags": {"tourism": "hotel", "name": "Rambagh Palace"},
                "source": "osm"
            },
            {
                "id": "node/445566",
                "name": "Central Park",
                "category": "leisure",
                "subcategory": "park",
                "coordinates": {"lat": 26.9201, "lon": 75.7873},
                "tags": {"leisure": "park", "name": "Central Park"},
                "source": "osm"
            },
            {
                "id": "way/556677",
                "name": "Sisodia Rani Garden",
                "category": "tourism",
                "subcategory": "attraction",
                "coordinates": {"lat": 26.8764, "lon": 75.8843},
                "tags": {"tourism": "attraction", "name": "Sisodia Rani Garden"},
                "source": "osm"
            }
        ]
        return mock_pois
    
    def _try_next_instance(self):
        """Switch to next Overpass instance"""
        self.current_instance = (self.current_instance + 1) % len(self.overpass_instances)
        self.base_url = self.overpass_instances[self.current_instance]
        self.api = overpy.Overpass(url=self.base_url)
        print(f"Switched to Overpass instance: {self.base_url}")
    
    def search_pois(
        self,
        city: str,
        categories: List[str] = None,
        limit: int = 50,
        max_retries: int = 3
    ) -> List[Dict]:
        """
        Search for Points of Interest in a city
        
        Args:
            city: City name (e.g., "Jaipur, India")
            categories: List of POI categories (e.g., ['tourism', 'amenity'])
            limit: Maximum number of results
            max_retries: Maximum number of retries with different instances
        
        Returns:
            List of POI dictionaries with OSM IDs
        """
        # Use mock data if enabled
        if self.use_mock:
            print(f"Using mock data for {city}")
            return self._get_mock_pois(city)[:limit]
        
        if categories is None:
            categories = ['tourism', 'amenity', 'historic', 'leisure']
        
        # Get city bounding box
        bbox = self.get_city_bbox(city)
        if not bbox:
            print(f"Could not find bounding box for {city}")
            # Fallback to mock data
            print("Falling back to mock data...")
            return self._get_mock_pois(city)[:limit]
        
        pois = []
        retry_count = 0
        
        # Try querying with retries across different instances
        while retry_count < max_retries and len(pois) < limit:
            try:
                # Expanded query - include more categories for better coverage
                query = f"""
                [out:json][timeout:25];
                (
                  node["tourism"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  way["tourism"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  node["historic"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  way["historic"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  node["amenity"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  way["amenity"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  node["shop"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  way["shop"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  node["leisure"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                  way["leisure"]["name"]({bbox["min_lat"]},{bbox["min_lon"]},{bbox["max_lat"]},{bbox["max_lon"]});
                );
                out center;
                """
                
                result = self.api.query(query)
                
                # Process nodes
                for node in result.nodes:
                    category = (
                        'tourism' if 'tourism' in node.tags else
                        'historic' if 'historic' in node.tags else
                        'amenity' if 'amenity' in node.tags else
                        'shop' if 'shop' in node.tags else
                        'leisure' if 'leisure' in node.tags else
                        'other'
                    )
                    poi = self._node_to_dict(node, category)
                    if poi:
                        pois.append(poi)
                
                # Process ways
                for way in result.ways:
                    category = (
                        'tourism' if 'tourism' in way.tags else
                        'historic' if 'historic' in way.tags else
                        'amenity' if 'amenity' in way.tags else
                        'shop' if 'shop' in way.tags else
                        'leisure' if 'leisure' in way.tags else
                        'other'
                    )
                    poi = self._way_to_dict(way, category)
                    if poi:
                        pois.append(poi)
                
                if len(pois) >= limit:
                    break  # Enough results
                    
            except Exception as e:
                error_msg = str(e).lower()
                if "timeout" in error_msg or "server load" in error_msg or "too high" in error_msg:
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"Server overloaded, trying next instance... (attempt {retry_count + 1}/{max_retries})")
                        self._try_next_instance()
                        continue
                    else:
                        print("All Overpass instances failed. Using mock data...")
                        return self._get_mock_pois(city)[:limit]
                else:
                    # Other error, try next instance
                    retry_count += 1
                    if retry_count < max_retries:
                        self._try_next_instance()
                        continue
        
        # If we still don't have enough, supplement with mock data
        # Aim for a reasonable minimum so multi-day itineraries don't run out
        min_required = min(15, limit)
        if len(pois) < min_required:
            print(f"Only found {len(pois)} POIs. Supplementing with mock data to reach {min_required}...")
            mock_pois = self._get_mock_pois(city)
            # Add mock POIs to fill the gap
            for mock_poi in mock_pois:
                if mock_poi['id'] not in [p['id'] for p in pois]:
                    pois.append(mock_poi)
                if len(pois) >= min_required:
                    break
        
        print(f"✅ Returning {len(pois)} POIs for {city}")
        return pois[:limit]
    
    def _node_to_dict(self, node, category: str) -> Optional[Dict]:
        """Convert Overpass node to POI dictionary"""
        tags = node.tags
        
        # Get name
        name = tags.get('name') or tags.get('name:en')
        if not name:
            return None
        
        # Get OSM ID
        osm_id = f"node/{node.id}"
        
        return {
            "id": osm_id,
            "name": name,
            "category": category,
            "subcategory": tags.get(category, ""),
            "coordinates": {
                "lat": float(node.lat),
                "lon": float(node.lon)
            },
            "tags": dict(tags),
            "source": "osm"
        }
    
    def _way_to_dict(self, way, category: str) -> Optional[Dict]:
        """Convert Overpass way to POI dictionary"""
        tags = way.tags
        
        # Get name
        name = tags.get('name') or tags.get('name:en')
        if not name:
            return None
        
        # Get center coordinates
        if hasattr(way, 'center_lat') and hasattr(way, 'center_lon'):
            lat, lon = way.center_lat, way.center_lon
        else:
            # Fallback: use first node
            if way.nodes:
                lat, lon = way.nodes[0].lat, way.nodes[0].lon
            else:
                return None
        
        # Get OSM ID
        osm_id = f"way/{way.id}"
        
        return {
            "id": osm_id,
            "name": name,
            "category": category,
            "subcategory": tags.get(category, ""),
            "coordinates": {
                "lat": float(lat),
                "lon": float(lon)
            },
            "tags": dict(tags),
            "source": "osm"
        }
    
    def get_poi_details(self, osm_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific POI by OSM ID
        
        Args:
            osm_id: OpenStreetMap ID (e.g., "way/123456" or "node/123456")
        
        Returns:
            POI details dictionary or None if not found
        """
        try:
            element_type, element_id = osm_id.split('/')
            query = f"""
            [out:json][timeout:25];
            {element_type}({element_id});
            out meta;
            """
            
            result = self.api.query(query)
            
            if element_type == "node" and result.nodes:
                return self._node_to_dict(result.nodes[0], "unknown")
            elif element_type == "way" and result.ways:
                return self._way_to_dict(result.ways[0], "unknown")
                
        except Exception as e:
            print(f"Error getting POI details for {osm_id}: {e}")
        
        return None
    
    def validate_poi_exists(self, osm_id: str) -> bool:
        """
        Validate that a POI exists in OSM dataset
        
        Args:
            osm_id: OpenStreetMap ID
        
        Returns:
            True if POI exists, False otherwise
        """
        poi = self.get_poi_details(osm_id)
        return poi is not None


# Test function
if __name__ == "__main__":
    client = OSMClient()
    
    # Test with Jaipur
    city = os.getenv("TARGET_CITY", "Jaipur, India")
    print(f"🔍 Searching POIs in {city}...")
    
    pois = client.search_pois(city, limit=10)
    print(f"\n✅ Found {len(pois)} POIs")
    
    for poi in pois[:5]:
        print(f"\n📍 {poi['name']}")
        print(f"   ID: {poi['id']}")
        print(f"   Category: {poi['category']}")
        print(f"   Location: {poi['coordinates']['lat']}, {poi['coordinates']['lon']}")
