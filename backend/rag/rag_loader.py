"""
RAG Loader - Populates vector store with travel guide data
"""
import os
import sys
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vector_store import VectorStore
from data_sources.wikivoyage_scraper import WikivoyageScraper
from rag.jaipur_data import JAIPUR_RAG_DATA, JAIPUR_POIS, JAIPUR_FESTIVALS

class RAGLoader:
    """
    Loads travel guide data into RAG vector store
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.wikivoyage_scraper = WikivoyageScraper()
    
    def load_city_data(self, city: str) -> Dict:
        """
        Load all data for a city into vector store
        
        Args:
            city: City name (e.g., "Jaipur")
        
        Returns:
            Statistics about loaded data
        """
        stats = {
            "city": city,
            "curated_chunks": 0,
            "wikivoyage_chunks": 0,
            "total_documents": 0,
            "errors": []
        }
        
        # Load curated data for Jaipur (only once to avoid duplicate/ redundant adds)
        if city.lower() in ["jaipur", "jaipur, india"]:
            print(f"📖 Loading curated RAG data for {city}...")
            try:
                # Skip if curated data already in store (check by known doc id)
                marker_id = "jaipur_amer_fort"
                existing = self.vector_store.collection.get(ids=[marker_id])
                if existing and existing.get("ids") and len(existing["ids"]) > 0:
                    print(f"   ⏭️  Curated data already in store, skipping duplicate load")
                    stats["curated_chunks"] = 0
                else:
                    self.vector_store.add_documents(JAIPUR_RAG_DATA)
                    stats["curated_chunks"] = len(JAIPUR_RAG_DATA)
                    print(f"   ✅ Loaded {len(JAIPUR_RAG_DATA)} curated chunks")
            except Exception as e:
                stats["errors"].append(f"Curated data error: {e}")
                print(f"   ❌ Error loading curated data: {e}")
                import traceback
                traceback.print_exc()
        
        # Also try Wikivoyage for additional data (skip if already loaded for this city)
        city_key = city.lower().replace(' ', '_').replace(',', '').strip()
        wv_marker_id = f"wikivoyage_{city_key}_see_0"
        try:
            existing_wv = self.vector_store.collection.get(ids=[wv_marker_id])
            if existing_wv and existing_wv.get("ids") and len(existing_wv["ids"]) > 0:
                print(f"   ⏭️  Wikivoyage data for {city} already in store, skipping")
            else:
                print(f"📖 Loading Wikivoyage data for {city}...")
                guide = self.wikivoyage_scraper.get_city_guide(city.split(',')[0].strip())
                
                if "error" in guide:
                    stats["errors"].append(f"Wikivoyage: {guide['error']}")
                    print(f"   ⚠️  Wikivoyage: {guide['error']}")
                else:
                    chunks = self.wikivoyage_scraper.chunk_by_section(guide)
                    
                    # Add unique IDs
                    for i, chunk in enumerate(chunks):
                        chunk["id"] = f"wikivoyage_{city_key}_{chunk['metadata']['section']}_{i}"
                    
                    if chunks:
                        self.vector_store.add_documents(chunks)
                        stats["wikivoyage_chunks"] = len(chunks)
                        print(f"   ✅ Loaded {len(chunks)} chunks from Wikivoyage")
                    else:
                        print(f"   ⚠️  No chunks extracted from Wikivoyage")
        
        except Exception as e:
            stats["errors"].append(f"Wikivoyage error: {e}")
            print(f"   ❌ Error: {e}")
        
        # Calculate total
        stats["total_documents"] = stats["curated_chunks"] + stats["wikivoyage_chunks"]
        
        return stats
    
    def load_poi_descriptions(self, pois: List[Dict]) -> Dict:
        """
        Load POI descriptions into vector store
        
        Args:
            pois: List of POIs with name, description, coordinates
        
        Returns:
            Statistics about loaded data
        """
        chunks = []
        
        for poi in pois:
            if poi.get("description"):
                chunk = {
                    "text": f"{poi['name']}: {poi['description']}",
                    "metadata": {
                        "type": "poi",
                        "poi_name": poi["name"],
                        "category": poi.get("category", "unknown"),
                        "source": "osm"
                    },
                    "id": f"poi_{poi.get('id', poi['name'].lower().replace(' ', '_'))}"
                }
                chunks.append(chunk)
        
        if chunks:
            self.vector_store.add_documents(chunks)
        
        return {
            "poi_chunks": len(chunks)
        }
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return self.vector_store.get_collection_stats()
    
    def get_jaipur_pois(self) -> List[Dict]:
        """Get curated Jaipur POIs"""
        return JAIPUR_POIS
    
    def get_jaipur_festivals(self) -> List[Dict]:
        """Get Jaipur festivals"""
        return JAIPUR_FESTIVALS


# Test function
if __name__ == "__main__":
    loader = RAGLoader()
    
    city = os.getenv("TARGET_CITY", "Jaipur")
    print(f"🔄 Loading RAG data for {city}...")
    print("=" * 50)
    
    stats = loader.load_city_data(city)
    
    print("\n" + "=" * 50)
    print("📊 Load Statistics:")
    print(f"   City: {stats['city']}")
    print(f"   Curated chunks: {stats['curated_chunks']}")
    print(f"   Wikivoyage chunks: {stats['wikivoyage_chunks']}")
    print(f"   Total documents: {stats['total_documents']}")
    
    if stats["errors"]:
        print(f"   Errors: {stats['errors']}")
    
    # Show collection stats
    collection_stats = loader.get_stats()
    print(f"\n📦 Vector Store Stats:")
    print(f"   Collection: {collection_stats['collection_name']}")
    print(f"   Total documents: {collection_stats['document_count']}")
    
    # Test query
    print("\n🔍 Testing RAG Query...")
    results = loader.vector_store.query("What is Hawa Mahal?", n_results=2)
    for i, result in enumerate(results):
        print(f"\n   Result {i+1}:")
        print(f"   Text: {result['text'][:100]}...")
        print(f"   Source: {result['metadata'].get('source', 'unknown')}")
    
    print("\n✅ RAG loader test complete!")
