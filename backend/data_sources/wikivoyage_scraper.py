"""
Wikivoyage scraper for city travel guides
"""
import requests
from typing import Dict, List
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv

load_dotenv()

class WikivoyageScraper:
    """
    Scraper for Wikivoyage travel guides
    """
    
    def __init__(self):
        self.base_url = "https://en.wikivoyage.org/wiki"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TravelPlanner/1.0 (Educational Project)'
        })
    
    def get_city_guide(self, city: str) -> Dict:
        """
        Get Wikivoyage guide for a city
        
        Args:
            city: City name (e.g., "Jaipur")
        
        Returns:
            Dictionary with guide sections and metadata
        """
        # Format city name for URL (capitalize, replace spaces with underscores)
        city_url = city.replace(' ', '_')
        url = f"{self.base_url}/{city_url}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if not content_div:
                return {"error": "Could not find content"}
            
            # Extract sections
            sections = self._extract_sections(content_div)
            
            return {
                "city": city,
                "url": url,
                "sections": sections,
                "source": "wikivoyage"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}
        except Exception as e:
            return {"error": f"Parsing failed: {e}"}
    
    def _extract_sections(self, content_div) -> Dict[str, List[Dict]]:
        """
        Extract sections from Wikivoyage content
        
        Common sections: Get in, See, Do, Eat, Stay, Stay safe, etc.
        """
        sections = {}
        current_section = None
        current_content = []
        
        # Find all headings (h2 and h3)
        for element in content_div.find_all(['h2', 'h3', 'p', 'ul', 'ol']):
            if element.name in ['h2', 'h3']:
                # Save previous section
                if current_section:
                    sections[current_section] = current_content
                
                # Start new section
                section_name = element.get_text().strip()
                # Remove "edit" links and clean up
                section_name = re.sub(r'\[edit\]', '', section_name).strip()
                current_section = section_name.lower().replace(' ', '_')
                current_content = []
            
            elif current_section and element.name in ['p', 'ul', 'ol']:
                # Extract text content
                text = element.get_text().strip()
                if text:
                    current_content.append({
                        "type": element.name,
                        "text": text,
                        "html": str(element)
                    })
        
        # Save last section
        if current_section:
            sections[current_section] = current_content
        
        return sections
    
    def chunk_by_section(self, guide: Dict) -> List[Dict]:
        """
        Chunk Wikivoyage guide by sections for RAG
        
        Args:
            guide: Guide dictionary from get_city_guide()
        
        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        if "error" in guide:
            return chunks
        
        city = guide.get("city", "Unknown")
        url = guide.get("url", "")
        sections = guide.get("sections", {})
        
        # Important sections for travel planning
        important_sections = [
            'see', 'do', 'eat', 'drink', 'buy', 'sleep',
            'stay_safe', 'get_in', 'get_around', 'understand'
        ]
        
        for section_name, content in sections.items():
            if section_name in important_sections:
                # Combine all content in section
                section_text = "\n\n".join([item["text"] for item in content])
                
                if section_text:
                    chunk = {
                        "text": section_text,
                        "metadata": {
                            "city": city,
                            "section": section_name,
                            "source": "wikivoyage",
                            "url": url,
                            "section_title": section_name.replace('_', ' ').title()
                        },
                        "source_url": url
                    }
                    chunks.append(chunk)
        
        return chunks


# Test function
if __name__ == "__main__":
    scraper = WikivoyageScraper()
    
    city = os.getenv("TARGET_CITY", "Jaipur")
    print(f"🔍 Fetching Wikivoyage guide for {city}...")
    
    guide = scraper.get_city_guide(city)
    
    if "error" in guide:
        print(f"❌ Error: {guide['error']}")
    else:
        print(f"✅ Guide fetched successfully!")
        print(f"   URL: {guide['url']}")
        print(f"   Sections: {list(guide['sections'].keys())[:5]}...")
        
        # Test chunking
        chunks = scraper.chunk_by_section(guide)
        print(f"\n✅ Created {len(chunks)} chunks for RAG")
