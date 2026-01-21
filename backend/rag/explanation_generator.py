"""
Explanation Generator - Uses RAG for grounded explanations
"""
import os
import sys
from typing import Dict, List, Optional, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vector_store import VectorStore
from llm.llm_client import LLMClient

class ExplanationGenerator:
    """
    Generates grounded explanations using RAG
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
    
    def explain_poi(self, poi_name: str, city: str) -> Dict[str, Any]:
        """
        Generate explanation for why a POI was selected
        
        Args:
            poi_name: Name of the POI
            city: City name
        
        Returns:
            Explanation with citations
        """
        # Query RAG for relevant information
        query = f"What is {poi_name} in {city}? Why should tourists visit?"
        rag_results = self.vector_store.query(
            query_text=query,
            n_results=3,
            filter_metadata={"city": city} if city else None
        )
        
        # Build context from RAG results
        context_parts = []
        citations = []
        
        for result in rag_results:
            context_parts.append(result["text"])
            citations.append({
                "text": result["text"][:100] + "...",
                "source": result["metadata"].get("source", "unknown"),
                "section": result["metadata"].get("section", "unknown"),
                "url": result["metadata"].get("url", "")
            })
        
        context = "\n\n".join(context_parts)
        
        # If no RAG results, note uncertainty
        if not context:
            return {
                "explanation": f"I selected {poi_name} as a popular attraction in {city}, but I don't have detailed information to explain why.",
                "citations": [],
                "grounded": False,
                "uncertainty": "No data available in knowledge base"
            }
        
        # Generate explanation using LLM with RAG context
        prompt = f"""
        Based on this information about {city}:
        
        {context}
        
        Explain why {poi_name} is a good place to visit in 2-3 sentences.
        Be specific and grounded in the information provided.
        If you're not sure about something, say so.
        """
        
        explanation = self.llm_client.call(
            prompt=prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        return {
            "explanation": explanation,
            "citations": citations,
            "grounded": True,
            "uncertainty": None
        }
    
    def explain_plan(
        self,
        question: str,
        itinerary: Dict,
        city: str
    ) -> Dict[str, Any]:
        """
        Answer questions about the plan (e.g., "Is this plan doable?")
        
        Args:
            question: User's question
            itinerary: The generated itinerary
            city: City name
        
        Returns:
            Answer with citations
        """
        # Query RAG for relevant information
        rag_results = self.vector_store.query(
            query_text=question,
            n_results=3
        )
        
        # Build context
        context_parts = []
        citations = []
        
        for result in rag_results:
            context_parts.append(result["text"])
            citations.append({
                "text": result["text"][:100] + "...",
                "source": result["metadata"].get("source", "unknown"),
                "section": result["metadata"].get("section", "unknown")
            })
        
        context = "\n\n".join(context_parts) if context_parts else "No specific information available."
        
        # Format itinerary summary
        itinerary_summary = self._format_itinerary_summary(itinerary)
        
        # Generate answer
        prompt = f"""
        You are a travel planning assistant. Answer this question about the travel plan:
        
        Question: "{question}"
        
        Itinerary:
        {itinerary_summary}
        
        Background information about {city}:
        {context}
        
        Answer the question in 2-3 sentences. Be specific and helpful.
        If you're not sure about something based on the available information, say so explicitly.
        """
        
        answer = self.llm_client.call(
            prompt=prompt,
            temperature=0.3,
            max_tokens=250
        )
        
        return {
            "answer": answer,
            "citations": citations,
            "grounded": len(citations) > 0
        }
    
    def explain_weather_impact(
        self,
        city: str,
        dates: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Explain weather considerations (e.g., "What if it rains?")
        
        Args:
            city: City name
            dates: Optional dates
        
        Returns:
            Weather considerations with citations
        """
        # Query RAG for weather/climate info
        query = f"weather climate {city} when to visit best time"
        rag_results = self.vector_store.query(
            query_text=query,
            n_results=3
        )
        
        context_parts = []
        citations = []
        
        for result in rag_results:
            context_parts.append(result["text"])
            citations.append({
                "text": result["text"][:100] + "...",
                "source": result["metadata"].get("source", "unknown"),
                "section": result["metadata"].get("section", "unknown")
            })
        
        context = "\n\n".join(context_parts)
        
        if not context:
            return {
                "explanation": f"I don't have specific weather information for {city}. Generally, it's good to check local weather forecasts and have indoor backup options.",
                "citations": [],
                "grounded": False,
                "uncertainty": "No weather data in knowledge base"
            }
        
        prompt = f"""
        Based on this information about {city}:
        
        {context}
        
        Explain what visitors should know about weather and climate in 2-3 sentences.
        Include any tips for dealing with weather changes.
        """
        
        explanation = self.llm_client.call(
            prompt=prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        return {
            "explanation": explanation,
            "citations": citations,
            "grounded": True
        }
    
    def _format_itinerary_summary(self, itinerary: Dict) -> str:
        """Format itinerary into readable summary"""
        if not itinerary or not itinerary.get("days"):
            return "No itinerary available"
        
        summary_parts = []
        for day in itinerary["days"]:
            day_summary = f"Day {day['day']} ({day.get('date', 'TBD')}):"
            for block in day.get("blocks", []):
                poi_names = [poi.get("poiId", "Unknown") for poi in block.get("pois", [])]
                if poi_names:
                    day_summary += f"\n  {block['type'].capitalize()}: {', '.join(poi_names)}"
            summary_parts.append(day_summary)
        
        return "\n".join(summary_parts)


# Test function
if __name__ == "__main__":
    generator = ExplanationGenerator()
    
    print("🧪 Testing Explanation Generator...")
    print("=" * 50)
    
    city = "Jaipur"
    
    # Test 1: Explain POI
    print("\n1️⃣  Explain POI: Hawa Mahal")
    result = generator.explain_poi("Hawa Mahal", city)
    print(f"   Explanation: {result['explanation'][:100]}...")
    print(f"   Citations: {len(result['citations'])}")
    print(f"   Grounded: {result['grounded']}")
    
    # Test 2: Plan question
    print("\n2️⃣  Plan Question: Is this plan doable?")
    test_itinerary = {
        "days": [
            {
                "day": 1,
                "date": "2024-01-20",
                "blocks": [
                    {"type": "morning", "pois": [{"poiId": "Hawa Mahal"}]},
                    {"type": "afternoon", "pois": [{"poiId": "City Palace"}]}
                ]
            }
        ]
    }
    result2 = generator.explain_plan("Is this plan doable?", test_itinerary, city)
    print(f"   Answer: {result2['answer'][:100]}...")
    print(f"   Grounded: {result2['grounded']}")
    
    # Test 3: Weather
    print("\n3️⃣  Weather: What if it rains?")
    result3 = generator.explain_weather_impact(city)
    print(f"   Explanation: {result3['explanation'][:100]}...")
    print(f"   Grounded: {result3['grounded']}")
    
    print("\n" + "=" * 50)
    print("✅ Explanation Generator test complete!")
