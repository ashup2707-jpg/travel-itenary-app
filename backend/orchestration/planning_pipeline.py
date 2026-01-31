"""
Planning Pipeline - Orchestrates the entire planning flow
Hybrid LLM + Symbolic architecture
"""
import os
import sys
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.intent_parser import IntentParser
from llm.constraint_collector import ConstraintCollector
from mcp_tools.poi_search.implementation import POISearchMCP
from mcp_tools.poi_search.schema import POISearchInput
from mcp_tools.itinerary_builder.implementation import ItineraryBuilderMCP
from mcp_tools.itinerary_builder.schema import ItineraryBuilderInput, TimeWindow
from rag.vector_store import VectorStore
from rag.rag_loader import RAGLoader
from rag.explanation_generator import ExplanationGenerator
from data_sources.wikivoyage_scraper import WikivoyageScraper
from edit.edit_parser import EditParser
from edit.edit_applier import EditApplier

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# POI name aliases: OSM / display names -> RAG canonical names (for better RAG matching)
POI_NAME_ALIASES = {
    "amber fort": "Amer Fort",
    "amer fort": "Amer Fort",
    "palace of winds": "Hawa Mahal",
    "hawa mahal": "Hawa Mahal",
    "city palace": "City Palace",
    "jantar mantar": "Jantar Mantar",
    "jal mahal": "Jal Mahal",
    "water palace": "Jal Mahal",
    "nahargarh": "Nahargarh Fort",
    "nahargarh fort": "Nahargarh Fort",
    "jaigarh": "Jaigarh Fort",
    "jaigarh fort": "Jaigarh Fort",
    "albert hall": "Albert Hall Museum",
    "albert hall museum": "Albert Hall Museum",
    "birla mandir": "Birla Mandir",
    "lakshmi narayan temple": "Birla Mandir",
    "galtaji": "Galtaji Temple",
    "galtaji temple": "Galtaji Temple",
    "monkey temple": "Galtaji Temple",
    "govind dev ji": "Govind Dev Ji Temple",
    "govind dev ji temple": "Govind Dev Ji Temple",
    "johari bazaar": "Johari Bazaar",
    "johari bazar": "Johari Bazaar",
    "bapu bazaar": "Bapu Bazaar",
    "bapu bazar": "Bapu Bazaar",
    "tripolia bazaar": "Tripolia Bazaar",
    "tripolia bazar": "Tripolia Bazaar",
    "chokhi dhani": "Chokhi Dhani",
    "rambagh palace": "Rambagh Palace",
    "sisodia rani garden": "Sisodia Rani Garden",
    "sisodia rani": "Sisodia Rani Garden",
    "central park": "Central Park",
    "ram niwas garden": "Ram Niwas Garden",
    "ram niwas": "Ram Niwas Garden",
    "laxmi mishthan bhandar": "Jaipur Food Guide",
    "lmb": "Jaipur Food Guide",
    "rawat mishthan": "Jaipur Food Guide",
}

def _normalize_poi_name_for_rag(raw_name: str) -> str:
    """Normalize POI name for RAG lookup: strip OSM ID prefix, apply aliases."""
    if not raw_name:
        return ""
    # Strip node/way/relation prefix (e.g. "node/123" -> use as-is for display but we need a name)
    s = str(raw_name).strip()
    for prefix in ("node/", "way/", "relation/"):
        if s.lower().startswith(prefix):
            return s  # Keep OSM ID if no display name; caller may have name separately
    key = s.lower().strip()
    return POI_NAME_ALIASES.get(key, s)

class PlanningPipeline:
    """
    Main planning pipeline
    Orchestrates intent parsing, constraint collection, POI search, itinerary building
    """
    
    def __init__(self, use_mock_data: bool = False):
        self.use_mock_data = use_mock_data
        
        # Initialize components
        self.intent_parser = IntentParser()
        self.constraint_collector = ConstraintCollector()
        self.poi_search_mcp = POISearchMCP(use_mock=use_mock_data)
        self.itinerary_builder_mcp = ItineraryBuilderMCP()
        self.rag_loader = RAGLoader()
        self.explanation_generator = ExplanationGenerator()
        self.edit_parser = EditParser()
        self.edit_applier = EditApplier(use_mock_data=use_mock_data)
        
        # Conversation state
        self.conversation_history: List[Dict] = []
        self.collected_constraints: Optional[Dict] = None
    
    def handle_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Handle user voice input
        
        Args:
            user_input: User's spoken request
        
        Returns:
            Response dictionary with action and data
        """
        # Step 1: Parse intent (LLM)
        intent = self.intent_parser.parse(user_input)
        
        # Merge with existing constraints if we have any
        if self.collected_constraints:
            # Update existing constraints with new information
            for key in ['city', 'duration', 'interests', 'pace', 'dates']:
                if intent.get(key) and not self.collected_constraints.get(key):
                    self.collected_constraints[key] = intent[key]
                elif intent.get(key):
                    self.collected_constraints[key] = intent[key]
            
            # Use merged constraints as the intent
            merged_intent = self.collected_constraints.copy()
            # Keep missing_info from new parse
            merged_intent['missing_info'] = intent.get('missing_info', [])
            intent = merged_intent
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "intent": intent
        })
        
        # Step 2: Collect constraints (LLM + Symbolic)
        constraint_result = self.constraint_collector.collect(
            intent,
            self.conversation_history
        )
        
        # Check what action to take
        if constraint_result["action"] == "ask":
            # Store partial constraints
            self.collected_constraints = constraint_result["constraints"]
            
            # Need to ask clarification question
            return {
                "action": "ask",
                "message": constraint_result["question"],
                "question_count": constraint_result["question_count"],
                "missing_info": constraint_result["missing_info"]
            }
        
        elif constraint_result["action"] == "max_reached":
            # Max questions reached, proceed with available info
            constraints = constraint_result["constraints"]
            self.collected_constraints = constraints
            
            if not constraints.get("city") or not constraints.get("duration"):
                return {
                    "action": "error",
                    "message": "Cannot proceed without city and duration. Please start over."
                }
            # Proceed with available constraints
        
        elif constraint_result["action"] == "proceed":
            # All constraints collected, proceed to planning
            constraints = constraint_result["constraints"]
            self.collected_constraints = constraints
        
        else:
            return {
                "action": "error",
                "message": "Unexpected constraint collection result"
            }
        
        # Step 3: Generate itinerary
        return self._generate_itinerary(constraints)
    
    def _generate_itinerary(self, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate itinerary from constraints
        
        Args:
            constraints: Collected constraints
        
        Returns:
            Response with itinerary or error
        """
        try:
            city = constraints.get("city") or os.getenv("TARGET_CITY", "Jaipur, India")
            interests = constraints.get("interests", [])
            duration = constraints.get("duration", 3)
            pace = constraints.get("pace", "moderate")
            
            # Step 1: Search POIs (POI Search MCP)
            poi_input = POISearchInput(
                city=city,
                interests=interests,
                constraints=constraints.get("constraints") or {}
            )
            
            poi_results = self.poi_search_mcp.search(poi_input)
            
            if len(poi_results.pois) == 0:
                return {
                    "action": "error",
                    "message": "Could not find any points of interest. Please try a different city or interests."
                }
            
            # Step 2: Load travel guidance (RAG)
            print(f"📖 Loading RAG data for {city.split(',')[0].strip()}...")
            rag_stats = self.rag_loader.load_city_data(city.split(',')[0].strip())  # Load city data into RAG
            print(f"   ✅ Loaded {rag_stats.get('total_documents', 0)} documents into RAG")
            
            # Check vector store stats
            vector_stats = self.rag_loader.get_stats()
            print(f"   📦 Vector store has {vector_stats.get('document_count', 0)} total documents")
            
            # Step 3: Create time windows
            time_windows = self._create_time_windows(duration, constraints.get("dates"))
            
            # Step 4: Build itinerary (Itinerary Builder MCP)
            pois_dict = [
                poi.model_dump() if hasattr(poi, 'model_dump') else poi.dict()
                for poi in poi_results.pois
            ]
            # Shuffle to avoid same fixed order every request
            random.shuffle(pois_dict)
            
            itinerary_input = ItineraryBuilderInput(
                pois=pois_dict,
                timeWindows=time_windows,
                constraints={
                    "maxTravelTimePerDay": 120,
                    "pace": pace,
                    "preferences": constraints.get("constraints") or {}
                }
            )
            
            itinerary_result = self.itinerary_builder_mcp.build(itinerary_input)
            
            # Step 5: Enrich itinerary with RAG data
            rag_citations = []
            rag_descriptions = {}
            
            # Check if vector store has data
            vector_stats = self.rag_loader.get_stats()
            total_docs = vector_stats.get('document_count', 0)
            print(f"   🔍 Vector store has {total_docs} documents available for querying")
            
            if total_docs == 0:
                print(f"   ⚠️  Warning: Vector store is empty! RAG data may not have loaded correctly.")
            else:
                # Query RAG for each POI in the itinerary to get descriptions and citations
                for day in itinerary_result.itinerary.days:
                    for block in day.blocks:
                        for poi_block in block.pois:
                            poi_name = poi_block.name or poi_block.poiId
                            # Normalize for RAG: use canonical name (e.g. Amber Fort -> Amer Fort)
                            canonical_name = _normalize_poi_name_for_rag(poi_name)
                            search_names = [poi_name, canonical_name]
                            search_names = list(dict.fromkeys([s for s in search_names if s]))
                            
                            # Query RAG for this POI - try multiple query variations
                            city_name = city.split(',')[0].strip()
                            rag_results = None
                            
                            # Try 1: Full descriptive query (try canonical name first)
                            for name in search_names:
                                rag_query = f"What is {name} in {city_name}? Why should tourists visit?"
                                rag_results = self.rag_loader.vector_store.query(
                                    query_text=rag_query,
                                    n_results=3
                                )
                                if rag_results:
                                    break
                            
                            # Try 2: Simple query with POI and city
                            if not rag_results:
                                for name in search_names:
                                    simple_query = f"{name} {city_name}"
                                    rag_results = self.rag_loader.vector_store.query(
                                        query_text=simple_query,
                                        n_results=3
                                    )
                                    if rag_results:
                                        break
                            
                            # Try 3: Just POI name
                            if not rag_results:
                                for name in search_names:
                                    rag_results = self.rag_loader.vector_store.query(
                                        query_text=name,
                                        n_results=3
                                    )
                                    if rag_results:
                                        break
                            
                            # Try 4: Search in metadata by POI name (exact match in metadata)
                            if not rag_results:
                                try:
                                    all_results = self.rag_loader.vector_store.query(
                                        query_text=city_name,
                                        n_results=50
                                    )
                                    rag_results = []
                                    poi_name_lower = poi_name.lower()
                                    canonical_lower = canonical_name.lower() if canonical_name else ""
                                    for result in all_results:
                                        result_poi_name = result.get("metadata", {}).get("poi_name", "").lower()
                                        if (poi_name_lower in result_poi_name or result_poi_name in poi_name_lower or
                                            (canonical_lower and (canonical_lower in result_poi_name or result_poi_name in canonical_lower))):
                                            rag_results.append(result)
                                            if len(rag_results) >= 3:
                                                break
                                except Exception as e:
                                    print(f"   ⚠️  Error in metadata search: {e}")
                            
                            # Try 5: Query with "tourist attraction" / "things to see" for better semantic match
                            if not rag_results:
                                for name in search_names:
                                    for template in [
                                        f"tourist attraction {name} {city_name}",
                                        f"things to see {name} {city_name}",
                                    ]:
                                        rag_results = self.rag_loader.vector_store.query(
                                            query_text=template,
                                            n_results=3
                                        )
                                        if rag_results:
                                            break
                                    if rag_results:
                                        break
                            # Try 6: POI name variations (short names, no Fort/Palace suffix)
                            if not rag_results:
                                for name in search_names:
                                    for variation in [name, name.lower(), name.replace(" ", "").lower(),
                                                     name.replace("Fort", "").strip(), name.replace("Palace", "").strip()]:
                                        if not variation:
                                            continue
                                        rag_results = self.rag_loader.vector_store.query(
                                            query_text=variation,
                                            n_results=3
                                        )
                                        if rag_results:
                                            break
                                    if rag_results:
                                        break
                            
                            if rag_results:
                                print(f"   ✅ Found RAG data for {poi_name}: {len(rag_results)} results")
                                # Prefer result that explicitly mentions this POI (metadata poi_name or text)
                                best = rag_results[0]
                                poi_lower = (canonical_name or poi_name).lower()
                                for r in rag_results:
                                    meta_poi = (r.get("metadata") or {}).get("poi_name", "").lower()
                                    if meta_poi and (poi_lower in meta_poi or meta_poi in poi_lower):
                                        best = r
                                        break
                                    if poi_lower and poi_lower in (r.get("text") or "").lower()[:200]:
                                        best = r
                                        break
                                # Store description from best-matching RAG result (280 chars for quality)
                                rag_descriptions[poi_block.poiId] = best["text"][:280] + ("..." if len(best["text"]) > 280 else "")
                                
                                # Collect citations
                                for result in rag_results:
                                    citation = {
                                        "poi": poi_name,
                                        "text": result["text"][:100] + "...",
                                        "source": result["metadata"].get("source", "unknown"),
                                        "section": result["metadata"].get("section", "unknown"),
                                        "url": result["metadata"].get("url", "")
                                    }
                                    # Avoid duplicate citations by checking source + poi combination
                                    is_duplicate = any(
                                        c.get("poi") == citation["poi"] and 
                                        c.get("source") == citation["source"] and
                                        c.get("section") == citation["section"]
                                        for c in rag_citations
                                    )
                                    if not is_duplicate:
                                        rag_citations.append(citation)
                            else:
                                print(f"   ⚠️  No RAG data found for {poi_name}")
                
                print(f"   📚 Collected {len(rag_citations)} RAG citations total")
            
            # Step 6: Store constraints for this itinerary
            self.collected_constraints = constraints
            
            # Return success with RAG data and POI list (for grounding eval and API state)
            pois_for_state = [
                p.model_dump() if hasattr(p, 'model_dump') else p.dict()
                for p in poi_results.pois
            ]
            return {
                "action": "itinerary",
                "itinerary": itinerary_result.itinerary.model_dump() if hasattr(itinerary_result.itinerary, 'model_dump') else itinerary_result.itinerary.dict(),
                "reasoning": itinerary_result.reasoning.model_dump() if hasattr(itinerary_result.reasoning, 'model_dump') else itinerary_result.reasoning.dict(),
                "poi_count": len(poi_results.pois),
                "pois": pois_for_state,
                "message": f"Created {duration}-day itinerary for {city}!",
                "rag_loaded": True,
                "rag_citations": rag_citations,
                "rag_descriptions": rag_descriptions
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "action": "error",
                "message": f"Error generating itinerary: {e}"
            }
    
    def explain(self, question: str, itinerary: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Answer questions about the itinerary in a grounded way. Handles:
        - "Why did you pick this place?" (POI or whole plan)
        - "Is this plan doable?" (feasibility + RAG)
        - "What if it rains?" (weather + indoor options)
        Always returns an answer with citations when possible; falls back to RAG-only if LLM fails.
        """
        if not self.collected_constraints and not itinerary:
            return {
                "action": "error",
                "message": "No itinerary to explain. Please create an itinerary first."
            }
        
        city = (self.collected_constraints or {}).get("city", "Jaipur")
        itinerary = itinerary or {}
        question_lower = question.lower().strip()

        # 1) Weather / rain
        if "rain" in question_lower or ("weather" in question_lower and ("if" in question_lower or "what" in question_lower)):
            result = self.explanation_generator.explain_weather_impact(city)
            return self._normalize_explain_response(result)
        # 2) Doable / feasible
        if "doable" in question_lower or "feasible" in question_lower or "realistic" in question_lower:
            result = self.explanation_generator.explain_plan(question, itinerary, city)
            return self._normalize_explain_response(result)
        # 3) Why pick / choose / select (this place or general)
        if "why" in question_lower and ("pick" in question_lower or "choose" in question_lower or "select" in question_lower):
            poi_name = self._extract_poi_from_question(question, itinerary)
            if poi_name:
                result = self.explanation_generator.explain_poi(poi_name, city)
                return self._normalize_explain_response(result)
            # No specific POI: explain selection for the plan (use itinerary + RAG)
            result = self.explanation_generator.explain_plan(question, itinerary, city)
            return self._normalize_explain_response(result)
        # 4) Any other question about the plan
        result = self.explanation_generator.explain_plan(question, itinerary, city)
        return self._normalize_explain_response(result)

    def _extract_poi_from_question(self, question: str, itinerary: Dict) -> Optional[str]:
        """Try to get a POI name from the question or from the itinerary."""
        # From itinerary: collect POI names for matching
        poi_names = []
        for day in (itinerary.get("days") or []):
            for block in day.get("blocks", []):
                for p in block.get("pois", []):
                    name = (p.get("name") or p.get("poiId") or "").strip()
                    if name and name not in poi_names:
                        poi_names.append(name)
        # Check if question mentions one of them (e.g. "why did you pick Hawa Mahal?")
        q = question.lower()
        for name in poi_names:
            if name.lower() in q:
                return name
        # Optionally: if only one POI in plan, return it
        if len(poi_names) == 1:
            return poi_names[0]
        return None

    def _normalize_explain_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure frontend always gets 'answer' and 'citations'."""
        answer = result.get("answer") or result.get("explanation") or ""
        citations = result.get("citations") or []
        out = {"action": "explanation", "answer": answer, "citations": citations, "grounded": result.get("grounded", True)}
        if result.get("explanation") and "explanation" not in out:
            out["explanation"] = result["explanation"]
        return out
    
    def handle_edit(self, edit_command: str, current_itinerary: Dict) -> Dict[str, Any]:
        """
        Handle voice-based edit command
        
        Args:
            edit_command: User's edit command (e.g., "Make Day 2 more relaxed")
            current_itinerary: Current itinerary to edit
        
        Returns:
            Updated itinerary with changes
        """
        if not self.collected_constraints:
            return {
                "action": "error",
                "message": "No itinerary to edit. Please create an itinerary first."
            }
        
        # Step 1: Parse edit command (LLM)
        edit_request = self.edit_parser.parse(edit_command, current_itinerary)
        
        if not edit_request.get("understood", False):
            return {
                "action": "clarify",
                "message": edit_request.get("clarification_needed", "Could not understand the edit. Please try again.")
            }
        
        # Step 2: Apply edit (Symbolic + MCP)
        result = self.edit_applier.apply(
            current_itinerary,
            edit_request,
            self.collected_constraints
        )
        
        if result["success"]:
            return {
                "action": "edit_applied",
                "itinerary": result["itinerary"],
                "changes": result["changes"],
                "message": f"Applied {result['edit_type']} edit to {result['scope']}"
            }
        else:
            return {
                "action": "error",
                "message": result.get("error", "Could not apply edit")
            }
    
    def _create_time_windows(
        self,
        duration: int,
        dates: Optional[Dict] = None
    ) -> List[TimeWindow]:
        """Create time windows for itinerary"""
        time_windows = []
        
        # Default start date (today + 1)
        if dates:
            # Handle dates as dict or string
            if isinstance(dates, dict) and dates.get("start"):
                base_date = datetime.fromisoformat(dates["start"])
            elif isinstance(dates, str):
                # Parse "January", "next week", etc. - use default for now
                base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            else:
                base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        else:
            base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        for day in range(1, duration + 1):
            day_date = base_date + timedelta(days=day - 1)
            
            time_windows.append(TimeWindow(
                day=day,
                morning={
                    "start": (day_date.replace(hour=9)).isoformat(),
                    "end": (day_date.replace(hour=12)).isoformat()
                },
                afternoon={
                    "start": (day_date.replace(hour=13)).isoformat(),
                    "end": (day_date.replace(hour=17)).isoformat()
                },
                evening={
                    "start": (day_date.replace(hour=18)).isoformat(),
                    "end": (day_date.replace(hour=21)).isoformat()
                }
            ))
        
        return time_windows


# Test function
if __name__ == "__main__":
    pipeline = PlanningPipeline(use_mock_data=True)
    
    print("🧪 Testing Planning Pipeline...")
    print("=" * 60)
    
    # Test 1: Initial request with missing info
    print("\n1️⃣  Test: Initial request (may need clarification)")
    result1 = pipeline.handle_user_input("Plan a trip to Jaipur")
    print(f"Action: {result1['action']}")
    if result1['action'] == 'ask':
        print(f"Question: {result1['message']}")
        print(f"Question count: {result1['question_count']}/6")
    
    # Test 2: Complete request
    print("\n2️⃣  Test: Complete request")
    result2 = pipeline.handle_user_input("Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace.")
    print(f"Action: {result2['action']}")
    if result2['action'] == 'itinerary':
        print(f"✅ Created itinerary with {len(result2['itinerary']['days'])} days")
        print(f"POIs used: {result2['poi_count']}")
    elif result2['action'] == 'error':
        print(f"❌ Error: {result2['message']}")
    
    print("\n" + "=" * 60)
    print("✅ Planning Pipeline Test Complete!")
