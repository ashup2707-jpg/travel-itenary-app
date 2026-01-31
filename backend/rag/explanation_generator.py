"""
Explanation Generator - Grounded explanations using RAG with robust LLM fallback
Answers: "Why did you pick this place?", "Is this plan doable?", "What if it rains?"
"""
import os
import sys
from typing import Dict, List, Optional, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vector_store import VectorStore

try:
    from llm.llm_client import LLMClient
    _LLM_AVAILABLE = True
except Exception:
    _LLM_AVAILABLE = False


def _normalize_response(out: Dict[str, Any], text_key: str = "answer") -> Dict[str, Any]:
    """Ensure response has 'answer' and 'citations' for frontend."""
    text = out.get("answer") or out.get("explanation") or ""
    out["answer"] = text
    if "explanation" not in out:
        out["explanation"] = text
    out.setdefault("citations", [])
    out.setdefault("grounded", len(out["citations"]) > 0)
    return out


class ExplanationGenerator:
    """
    Generates grounded explanations using RAG. Falls back to RAG-only when LLM
    is unavailable or fails, so every query gets a genuine, grounded answer.
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_client = None
        if _LLM_AVAILABLE:
            try:
                self.llm_client = LLMClient()
            except Exception as e:
                print(f"ExplanationGenerator: LLM not available ({e}), using RAG-only fallback.")

    def _rag_query(self, query_text: str, n_results: int = 5, filter_metadata: Optional[Dict] = None) -> tuple:
        """Return (context_string, citations_list)."""
        results = self.vector_store.query(
            query_text=query_text,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
        context_parts = []
        citations = []
        for r in results:
            context_parts.append(r["text"])
            citations.append({
                "text": (r["text"][:120] + "...") if len(r.get("text", "")) > 120 else r.get("text", ""),
                "source": (r.get("metadata") or {}).get("source", "unknown"),
                "section": (r.get("metadata") or {}).get("section", "unknown"),
                "url": (r.get("metadata") or {}).get("url", ""),
            })
        return "\n\n".join(context_parts), citations

    def explain_poi(self, poi_name: str, city: str) -> Dict[str, Any]:
        """
        Why was this place picked? Grounded in RAG; fallback to RAG-only if LLM fails.
        """
        city_clean = (city or "").split(",")[0].strip() or "Jaipur"
        query = f"Why should tourists visit {poi_name} in {city_clean}? What is {poi_name}?"
        context, citations = self._rag_query(query, n_results=4, filter_metadata={"city": city_clean} if city_clean else None)

        if not context:
            return _normalize_response({
                "explanation": f"I picked {poi_name} as a key attraction in {city_clean}. I don't have extra detail in my sources to explain further.",
                "citations": [],
                "grounded": False,
            })

        if self.llm_client:
            try:
                prompt = f"""Based only on this information about {city_clean}:

{context}

In 2-3 sentences, explain why {poi_name} is a good choice for this itinerary. Be specific and cite the information above. Do not make up facts."""
                explanation = self.llm_client.call(prompt=prompt, temperature=0.3, max_tokens=220)
                if explanation and explanation.strip():
                    return _normalize_response({
                        "explanation": explanation.strip(),
                        "citations": citations,
                        "grounded": True,
                    })
            except Exception as e:
                print(f"ExplanationGenerator explain_poi LLM fallback: {e}")

        # RAG-only fallback: use first chunk as basis
        first = context.split("\n\n")[0].strip()
        if len(first) > 400:
            first = first[:397] + "..."
        return _normalize_response({
            "explanation": f"For {poi_name}: {first}",
            "citations": citations,
            "grounded": True,
        })

    def explain_plan(
        self,
        question: str,
        itinerary: Dict,
        city: str
    ) -> Dict[str, Any]:
        """
        Is this plan doable? / general plan questions. Uses itinerary (days, feasibility, travel)
        plus RAG; fallback to RAG + itinerary stats if LLM fails.
        """
        city_clean = (city or "").split(",")[0].strip() or "Jaipur"
        summary = self._format_itinerary_summary(itinerary)
        stats = self._itinerary_stats(itinerary)

        # RAG: doable, feasible, get around, suggested itinerary
        q1, c1 = self._rag_query(f"is a multi-day plan doable feasible {city_clean} itinerary get around travel time", n_results=4)
        q2, c2 = self._rag_query(f"suggested itinerary {city_clean} days", n_results=2)
        context = "\n\n".join(filter(None, [q1, q2]))
        citations = c1 + [x for x in c2 if x not in c1][:2]

        if self.llm_client and context:
            try:
                prompt = f"""You are a travel assistant. Answer this question about the plan using ONLY the itinerary and background below.

Question: "{question}"

Itinerary:
{summary}
{stats}

Background about {city_clean}:
{context}

Answer in 2-4 sentences. Be specific: mention days, places, or travel time from the itinerary. Say if something is uncertain."""
                answer = self.llm_client.call(prompt=prompt, temperature=0.3, max_tokens=280)
                if answer and answer.strip():
                    return _normalize_response({
                        "answer": answer.strip(),
                        "citations": citations,
                        "grounded": True,
                    })
            except Exception as e:
                print(f"ExplanationGenerator explain_plan LLM fallback: {e}")

        # RAG + stats fallback
        parts = []
        if stats:
            parts.append(stats)
        if context:
            parts.append(context[:500] + ("..." if len(context) > 500 else ""))
        answer = " ".join(parts) if parts else "I don't have enough data to say; generally a 2–3 day Jaipur plan is doable with 2–3 sights per day and some travel time."
        return _normalize_response({
            "answer": answer,
            "citations": citations,
            "grounded": len(citations) > 0,
        })

    def explain_weather_impact(self, city: str, dates: Optional[Dict] = None) -> Dict[str, Any]:
        """
        What if it rains? Weather / rain / indoor options. RAG-first; LLM optional.
        """
        city_clean = (city or "").split(",")[0].strip() or "Jaipur"
        q1, c1 = self._rag_query(f"weather climate {city_clean} best time monsoon rain", n_results=3)
        q2, c2 = self._rag_query(f"rainy day indoor activities {city_clean} what if it rains", n_results=3)
        context = "\n\n".join(filter(None, [q1, q2]))
        citations = c1 + [x for x in c2 if x not in c1][:3]

        if not context:
            return _normalize_response({
                "explanation": f"I don't have specific weather data for {city_clean}. Check local forecasts; have indoor options like museums or markets.",
                "citations": [],
                "grounded": False,
            })

        if self.llm_client:
            try:
                prompt = f"""Using only this information about {city_clean}:

{context}

In 2-4 sentences, tell the visitor what to expect about weather and what to do if it rains. Be specific (e.g. indoor options, monsoon timing)."""
                explanation = self.llm_client.call(prompt=prompt, temperature=0.3, max_tokens=220)
                if explanation and explanation.strip():
                    return _normalize_response({
                        "explanation": explanation.strip(),
                        "citations": citations,
                        "grounded": True,
                    })
            except Exception as e:
                print(f"ExplanationGenerator explain_weather LLM fallback: {e}")

        # RAG-only
        first = context.split("\n\n")[0].strip()
        if len(first) > 380:
            first = first[:377] + "..."
        return _normalize_response({
            "explanation": first,
            "citations": citations,
            "grounded": True,
        })

    def _format_itinerary_summary(self, itinerary: Dict) -> str:
        if not itinerary or not itinerary.get("days"):
            return "No itinerary available"
        parts = []
        for day in itinerary["days"]:
            day_line = f"Day {day.get('day', '?')} ({day.get('date', 'TBD')}):"
            for block in day.get("blocks", []):
                pois = block.get("pois", [])
                names = [p.get("name") or p.get("poiId", "?") for p in pois]
                if names:
                    day_line += f" {block.get('type', '')} – {', '.join(names)}."
            parts.append(day_line)
        return "\n".join(parts)

    def _itinerary_stats(self, itinerary: Dict) -> str:
        """Short stats line for doable/feasibility answers."""
        if not itinerary or not itinerary.get("days"):
            return ""
        days = itinerary["days"]
        total_travel = 0
        total_pois = 0
        feas = []
        for d in days:
            total_travel += d.get("totalTravelTime") or 0
            for b in d.get("blocks", []):
                total_pois += len(b.get("pois", []))
            s = d.get("feasibilityScore")
            if s is not None:
                feas.append(f"Day {d.get('day')}: {int(s * 100)}%")
        line = f"Plan: {len(days)} days, {total_pois} places."
        if total_travel:
            line += f" Total travel: {total_travel} min."
        if feas:
            line += f" Feasibility: {', '.join(feas)}."
        return line


# Test
if __name__ == "__main__":
    gen = ExplanationGenerator()
    city = "Jaipur"
    print("1. Explain POI:", gen.explain_poi("Hawa Mahal", city).get("answer", "")[:150])
    print("2. Explain plan:", gen.explain_plan("Is this plan doable?", {"days": [{"day": 1, "blocks": [{"type": "morning", "pois": [{"poiId": "Hawa Mahal"}]}]}]}, city).get("answer", "")[:150])
    print("3. Weather:", gen.explain_weather_impact(city).get("answer", "")[:150])
