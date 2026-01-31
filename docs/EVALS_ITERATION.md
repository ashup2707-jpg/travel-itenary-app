# AI Evals & Iteration

How to run evaluations and use them to iterate on prompts, RAG, and MCP.

---

## Run evals via API (after creating a plan)

1. **Create an itinerary** in the app (e.g. "Plan a 3-day trip to Jaipur. I like food and culture.").
2. **Run all evals** (feasibility + grounding on current state):

   ```bash
   curl -s http://localhost:8000/api/eval/all
   ```

   Returns: `all_passed`, `average_score`, `results.feasibility`, `results.grounding`.

3. **Run single evals:**
   - Feasibility: `curl -X POST http://localhost:8000/api/eval/feasibility`
   - Grounding: `curl -X POST http://localhost:8000/api/eval/grounding`
   - Edit correctness: `POST /api/eval/edit` with body `{ original, edited, edit_request, changes }` (e.g. after applying an edit).

---

## Run evals from code (backend)

```bash
cd backend
python3 -c "
from evaluations import FeasibilityEval, GroundingEval
from orchestration.planning_pipeline import PlanningPipeline

# Build a minimal itinerary and constraints (or use current_state from API)
itinerary = {'days': [{'day': 1, 'blocks': [{'type': 'morning', 'pois': [{'poiId': 'node/1', 'name': 'Hawa Mahal'}]}]}]}
constraints = {'city': 'Jaipur', 'duration': 3, 'interests': ['culture'], 'pace': 'moderate'}
pois = [{'id': 'node/1', 'name': 'Hawa Mahal'}]
explanations = []

feas = FeasibilityEval()
print('Feasibility:', feas.run(itinerary, constraints))

ground = GroundingEval()
print('Grounding:', ground.run(itinerary, pois, explanations))
"
```

---

## What each eval checks

| Eval | What it checks |
|------|----------------|
| **Feasibility** | Daily duration ≤ 12h; travel time ≤ 40% of total; POI count matches pace. |
| **Edit correctness** | Only the intended day/block changed; no unintended edits. |
| **Grounding** | POIs have valid OSM IDs; explanations have citations; uncertainty stated when needed. |

---

## Iteration loop

1. **Run evals** (API or code above). Note `passed` and `score` for each.
2. **If feasibility fails:** Adjust itinerary builder constraints (e.g. `maxTravelTimePerDay`, pace limits) in `mcp_tools/itinerary_builder/implementation.py` or symbolic `feasibility_engine.py`.
3. **If grounding fails:** Add or refine RAG chunks in `rag/jaipur_data.py`; add POI name aliases in `planning_pipeline.py`; tighten explanation prompts in `rag/explanation_generator.py`.
4. **If edit correctness fails:** Refine edit parser prompts in `edit/edit_parser.py` or edit applier logic in `edit/edit_applier.py`.
5. **Re-run evals** and repeat until scores and `passed` are acceptable.

---

## Quick reference

- **API base:** `http://localhost:8000` (or your deployed backend URL).
- **Eval endpoints:** `GET /api/eval/all`, `POST /api/eval/feasibility`, `POST /api/eval/grounding`, `POST /api/eval/edit`.
- **Code:** `backend/evaluations/` — `feasibility_eval.py`, `edit_correctness_eval.py`, `grounding_eval.py`; see `evaluations/README.md`.
