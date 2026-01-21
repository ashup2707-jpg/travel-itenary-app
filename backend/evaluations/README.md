# Evaluations

This module contains the three required evaluation systems.

## 1. Feasibility Evaluation (`feasibility_eval.py`)

Checks itinerary feasibility:
- **Daily duration** ≤ available time (12 hours)
- **Travel time** ≤ 40% of total time
- **Pace consistency** - POI count matches pace setting

### Run Evaluation

```bash
cd backend
python3 evaluations/feasibility_eval.py
```

## 2. Edit Correctness Evaluation (`edit_correctness_eval.py`)

Checks that voice edits only modify intended sections:
- **Intended changes** were made
- **No unintended changes** outside edit scope

### Run Evaluation

```bash
cd backend
python3 evaluations/edit_correctness_eval.py
```

## 3. Grounding & Hallucination Evaluation (`grounding_eval.py`)

Checks factual accuracy:
- **POI grounding** - POIs map to OSM records
- **Citation presence** - Explanations cite RAG sources
- **Uncertainty handling** - Missing data is acknowledged

### Run Evaluation

```bash
cd backend
python3 evaluations/grounding_eval.py
```

## Using in Code

```python
from evaluations import FeasibilityEval, EditCorrectnessEval, GroundingEval

# Feasibility
feasibility_eval = FeasibilityEval()
result = feasibility_eval.run(itinerary, constraints)

# Edit Correctness
edit_eval = EditCorrectnessEval()
result = edit_eval.run(original, edited, edit_request, changes)

# Grounding
grounding_eval = GroundingEval()
result = grounding_eval.run(itinerary, pois, explanations)
```

## Evaluation Results

All evaluations return:
- `passed`: Boolean
- `score`: Float (0.0 - 1.0)
- `checks`: Detailed check results
