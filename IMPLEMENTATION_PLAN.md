# Implementation Plan: Voice-First AI Travel Planning Assistant

**Architecture:** Hybrid LLM + Symbolic  
**Timeline:** 6-8 weeks (recommended) or 4-5 weeks (accelerated)  
**Target City:** Jaipur (or your chosen city)

---

## Overview

This plan implements a capstone-grade voice-first travel planning assistant using Hybrid LLM + Symbolic architecture. The system will:
- Handle natural voice conversations (LLM layer)
- Enforce feasibility constraints rigorously (Symbolic layer)
- Support partial itinerary edits
- Provide grounded explanations with citations
- Integrate MCP tools and RAG systems
- Pass comprehensive evaluations

---

## Phase 1: Foundation & Infrastructure (Week 1-2)

### 1.1 Project Setup

**Tasks:**
- [ ] Initialize git repository
- [ ] Set up project structure (backend + frontend)
- [ ] Choose tech stack:
  - **Backend:** Python (FastAPI) or Node.js (Express)
  - **Frontend:** React/Next.js (for Lovable) or vanilla JS
  - **LLM API:** OpenAI GPT-4 or Anthropic Claude
  - **Vector DB:** Chroma (local) or Pinecone/Weaviate (cloud)
  - **Voice:** Web Speech API or Deepgram/AssemblyAI
- [ ] Set up environment variables and config files
- [ ] Create README with architecture overview

**Deliverable:** Project skeleton with basic structure

---

### 1.2 Voice Interface Layer

**Tasks:**
- [ ] Implement Speech-to-Text (STT)
  - Option A: Web Speech API (browser-based, free)
  - Option B: Deepgram/AssemblyAI API (more accurate, paid)
- [ ] Implement Text-to-Speech (TTS)
  - Option A: Web Speech API (browser-based)
  - Option B: ElevenLabs/Google TTS (better quality)
- [ ] Create microphone button component
- [ ] Implement live transcript display
- [ ] Add voice activity detection (VAD)
- [ ] Handle interruptions and corrections

**Deliverable:** Working voice input/output with live transcript

**Files to Create:**
```
frontend/
  components/
    MicrophoneButton.tsx
    LiveTranscript.tsx
  utils/
    speechToText.ts
    textToSpeech.ts
```

---

### 1.3 Data Source Setup

**Tasks:**
- [ ] **OpenStreetMap Integration**
  - Set up Overpass API client
  - Create POI query functions (by city, category, location)
  - Store POI IDs for grounding validation
  - Test with Jaipur (or target city)
- [ ] **Wikivoyage/Wikipedia Integration**
  - Scrape or use API for city guide
  - Chunk by section (Get in, See, Do, Eat, Stay, Stay safe)
  - Store chunks with metadata (section, source URL)
- [ ] **RAG Vector Store Setup**
  - Initialize vector database (Chroma/Pinecone)
  - Create embedding pipeline
  - Index Wikivoyage chunks
  - Index Wikipedia chunks (if using)
  - Create multi-store routing logic

**Deliverable:** Data sources integrated, RAG system ready

**Files to Create:**
```
backend/
  data_sources/
    osm_client.py (or .js)
    wikivoyage_scraper.py
    wikipedia_client.py
  rag/
    vector_store.py
    chunking_strategy.py
    query_router.py
```

---

## Phase 2: Core Planning System (Week 3-4)

### 2.1 LLM Intent & Dialogue Management

**Tasks:**
- [ ] **Intent Parser (LLM)**
  - Create prompt for extracting structured intent from voice input
  - Extract: city, duration, interests, pace, dates
  - Handle ambiguous inputs gracefully
- [ ] **Constraint Collector (LLM + Symbolic)**
  - LLM identifies missing information
  - LLM generates natural clarification questions
  - Symbolic counter enforces max 6 questions
  - Symbolic validator confirms all required constraints
- [ ] **Conversation State Management**
  - Track collected constraints
  - Track question count
  - Maintain conversation context

**Deliverable:** Natural conversation flow with constraint collection

**Files to Create:**
```
backend/
  llm/
    intent_parser.py
    constraint_collector.py
    conversation_manager.py
  symbolic/
    question_counter.py
    constraint_validator.py
```

**Example Implementation:**
```python
# constraint_collector.py
def collect_constraints(user_input, current_state):
    # LLM identifies missing info
    missing = llm_identify_missing(user_input, current_state)
    
    # Check question count (symbolic)
    if current_state.question_count >= 6:
        return {"action": "proceed", "message": "Max questions reached"}
    
    if missing:
        question = llm_generate_question(missing)
        return {
            "action": "ask",
            "question": question,
            "question_count": current_state.question_count + 1
        }
    else:
        # Validate all constraints present (symbolic)
        if validate_constraints(current_state):
            return {"action": "proceed", "message": "Ready to plan"}
        else:
            return {"action": "ask", "question": "Please confirm your constraints"}
```

---

### 2.2 MCP Tool: POI Search

**Tasks:**
- [ ] **Design Strict Schema**
  - Input: city, interests[], constraints{}, timeWindow?
  - Output: POIs[] with OSM IDs, metadata, source
- [ ] **Implement POI Search MCP**
  - Query OSM Overpass API
  - Filter by interests and constraints
  - Rank POIs by relevance
  - Return structured output with OSM IDs
- [ ] **Add Validation Layer**
  - Validate input schema
  - Validate output schema
  - Log all tool calls

**Deliverable:** Working POI Search MCP with strict schemas

**Files to Create:**
```
backend/
  mcp_tools/
    poi_search/
      schema.py (input/output types)
      implementation.py
      validator.py
```

**Schema Example:**
```python
# schema.py
from pydantic import BaseModel
from typing import Optional, List

class POISearchInput(BaseModel):
    city: str
    interests: List[str]  # max 10
    constraints: dict  # maxDistance, accessibility, budget, etc.
    timeWindow: Optional[dict] = None

class POI(BaseModel):
    id: str  # OSM ID (required)
    name: str
    category: str
    coordinates: dict  # {lat, lon}
    estimatedDuration: int  # minutes
    openingHours: Optional[str] = None
    source: str  # "osm" or "wikivoyage"
    metadata: dict

class POISearchOutput(BaseModel):
    pois: List[POI]
    totalFound: int
    queryTime: str  # ISO8601
```

---

### 2.3 Symbolic Feasibility Engine

**Tasks:**
- [ ] **Time Calculations**
  - POI duration estimates
  - Travel time between POIs (heuristic or API)
  - Total daily time calculation
- [ ] **Distance Calculations**
  - Geographic distance between POIs
  - Route optimization (simple heuristic)
- [ ] **Pace Analysis**
  - "Relaxed" = fewer POIs, more rest time
  - "Moderate" = balanced
  - "Fast" = more POIs, less rest
- [ ] **Constraint Satisfaction**
  - Check all constraints satisfied
  - Identify violations
  - Generate feasibility score

**Deliverable:** Rigorous feasibility analysis engine

**Files to Create:**
```
backend/
  symbolic/
    feasibility_engine.py
    time_calculator.py
    distance_calculator.py
    pace_analyzer.py
```

**Example Implementation:**
```python
# feasibility_engine.py
def analyze_feasibility(pois, time_windows, constraints):
    """
    Symbolic feasibility analysis
    """
    violations = []
    
    for day, time_window in enumerate(time_windows, 1):
        # Calculate total time needed
        total_poi_time = sum(poi.duration for poi in pois)
        total_travel_time = calculate_travel_time(pois)
        total_time = total_poi_time + total_travel_time
        
        # Check against available time
        available_time = (
            time_window['evening']['end'] - 
            time_window['morning']['start']
        ).total_seconds() / 60  # minutes
        
        if total_time > available_time:
            violations.append({
                "type": "time_exceeded",
                "day": day,
                "needed": total_time,
                "available": available_time
            })
        
        # Check travel time ratio (pace consistency)
        travel_ratio = total_travel_time / total_time if total_time > 0 else 0
        if travel_ratio > 0.4:  # >40% travel time
            violations.append({
                "type": "excessive_travel",
                "day": day,
                "ratio": travel_ratio
            })
    
    return {
        "feasible": len(violations) == 0,
        "violations": violations,
        "score": 1.0 - (len(violations) / max_violations)
    }
```

---

### 2.4 MCP Tool: Itinerary Builder

**Tasks:**
- [ ] **Design Strict Schema**
  - Input: POIs[], timeWindows[], constraints{}
  - Output: structured itinerary with days, blocks, POIs, times
- [ ] **Implement Itinerary Builder MCP**
  - Take candidate POIs from POI Search
  - Apply feasibility analysis
  - Generate day-wise itinerary with time blocks
  - Assign POIs to morning/afternoon/evening blocks
  - Calculate arrival/departure times
  - Generate reasoning for each decision
- [ ] **Add Validation**
  - Validate all POIs have OSM IDs
  - Validate time windows respected
  - Validate constraints satisfied

**Deliverable:** Working Itinerary Builder MCP

**Files to Create:**
```
backend/
  mcp_tools/
    itinerary_builder/
      schema.py
      implementation.py
      validator.py
```

---

### 2.5 Planning Pipeline Integration

**Tasks:**
- [ ] **Orchestrate Planning Flow**
  - User input → Intent Parser
  - Constraint Collection (max 6 questions)
  - POI Search MCP call
  - RAG query for travel guidance
  - Feasibility Engine analysis
  - Itinerary Builder MCP call
  - Pre-response evals
- [ ] **Error Handling**
  - Handle MCP tool failures
  - Handle RAG failures
  - Graceful degradation
- [ ] **Logging**
  - Log all MCP tool calls (for demo)
  - Log all RAG queries
  - Log feasibility analysis

**Deliverable:** End-to-end planning pipeline

**Files to Create:**
```
backend/
  orchestration/
    planning_pipeline.py
    error_handler.py
    logger.py
```

---

## Phase 3: Edit System & Explanations (Week 5)

### 3.1 Edit Parser & Scoping

**Tasks:**
- [ ] **LLM Edit Parser**
  - Parse edit requests ("Make Day 2 more relaxed")
  - Extract edit intent and scope
  - Identify affected sections (Day 2, Day 1 Evening, etc.)
- [ ] **Symbolic Scope Validator**
  - Validate scope is reasonable
  - Prevent full regeneration
  - Confirm only intended sections affected
- [ ] **Edit Representation**
  - Create edit plan structure
  - Track dependencies between sections

**Deliverable:** Edit parsing and scoping system

**Files to Create:**
```
backend/
  llm/
    edit_parser.py
  symbolic/
    scope_validator.py
    edit_planner.py
```

**Example Implementation:**
```python
# edit_parser.py
def parse_edit(user_input, current_itinerary):
    """
    LLM parses edit request and identifies scope
    """
    prompt = f"""
    User wants to edit itinerary: "{user_input}"
    Current itinerary has {len(current_itinerary.days)} days.
    
    Identify:
    1. What sections are affected? (e.g., "Day 2", "Day 1 evening")
    2. What operation? (e.g., "reduce_pace", "swap", "add")
    3. What constraints changed?
    
    Return JSON:
    {{
        "scope": ["Day 2"],
        "operation": "reduce_pace",
        "constraints": {{"pace": "relaxed"}}
    }}
    """
    
    response = llm_call(prompt)
    return parse_json(response)

# scope_validator.py
def validate_scope(edit_plan, current_itinerary):
    """
    Symbolic validation of edit scope
    """
    # Check scope is not too broad
    affected_days = set()
    for section in edit_plan.scope:
        if section.startswith("Day"):
            day_num = int(section.split()[1])
            affected_days.add(day_num)
    
    # Reject if more than 50% of days affected
    if len(affected_days) > len(current_itinerary.days) * 0.5:
        return {
            "valid": False,
            "reason": "Scope too broad - would regenerate too much"
        }
    
    return {"valid": True}
```

---

### 3.2 Partial Regeneration

**Tasks:**
- [ ] **Partial Regenerator**
  - Regenerate only affected sections
  - Use POI Search MCP for new POIs (if needed)
  - Use Itinerary Builder MCP for affected sections only
  - Preserve unchanged sections
- [ ] **Merge Handler**
  - Merge regenerated sections with unchanged sections
  - Validate merged itinerary
  - Track diffs for explanation

**Deliverable:** Working partial regeneration system

**Files to Create:**
```
backend/
  edit/
    partial_regenerator.py
    merge_handler.py
    diff_tracker.py
```

---

### 3.3 Explanation Generator

**Tasks:**
- [ ] **LLM Explanation Generator**
  - Generate natural explanations for decisions
  - Answer "Why did you pick this place?"
  - Answer "Is this plan doable?"
  - Answer "What if it rains?"
- [ ] **RAG Integration for Grounding**
  - Query RAG for relevant context
  - Use Wikivoyage/Wikipedia for explanations
  - Append citations automatically
- [ ] **Citation Enforcement**
  - Ensure every fact has citation
  - Handle missing data explicitly
  - Format citations for UI

**Deliverable:** Grounded explanation system with citations

**Files to Create:**
```
backend/
  llm/
    explanation_generator.py
  rag/
    explanation_rag.py
  symbolic/
    citation_enforcer.py
```

**Example Implementation:**
```python
# explanation_generator.py
def generate_explanation(question, context, itinerary):
    """
    Generate grounded explanation with citations
    """
    # Query RAG for relevant context
    rag_results = query_rag(question, context)
    
    # Generate explanation using LLM + RAG context
    prompt = f"""
    User asks: "{question}"
    
    Context from travel guides:
    {rag_results.text}
    
    Itinerary context:
    {itinerary.summary}
    
    Generate a natural explanation. Include citations from the travel guides.
    """
    
    explanation = llm_call(prompt)
    
    # Enforce citations (symbolic)
    citations = [r.source_url for r in rag_results]
    if not citations:
        explanation += " [Note: Limited information available]"
    else:
        explanation += f" [Sources: {', '.join(citations)}]"
    
    return {
        "explanation": explanation,
        "citations": citations
    }
```

---

## Phase 4: Evaluation System (Week 5-6)

### 4.1 Feasibility Evaluation

**Tasks:**
- [ ] **Implement Feasibility Eval**
  - Check daily duration ≤ available time
  - Check reasonable travel times
  - Check pace consistency
  - Return violations and score
- [ ] **Integration**
  - Run before returning itinerary to user
  - Hard block if violations found
  - Log results

**Deliverable:** Working feasibility evaluation

**Files to Create:**
```
backend/
  evaluations/
    feasibility_eval.py
```

**Implementation:**
```python
# feasibility_eval.py
def evaluate_feasibility(itinerary, constraints):
    violations = []
    
    for day in itinerary.days:
        # Check total time
        total_time = sum(block.totalDuration for block in day.blocks)
        if total_time > constraints.maxTimePerDay:
            violations.append({
                "type": "time_exceeded",
                "day": day.day,
                "actual": total_time,
                "max": constraints.maxTimePerDay
            })
        
        # Check travel time
        for block in day.blocks:
            if block.travelTime > constraints.maxTravelTimePerBlock:
                violations.append({
                    "type": "excessive_travel",
                    "day": day.day,
                    "block": block.type,
                    "travel_time": block.travelTime
                })
        
        # Check pace consistency
        travel_ratio = day.totalTravelTime / day.totalDuration
        if travel_ratio > 0.4:
            violations.append({
                "type": "pace_inconsistent",
                "day": day.day,
                "travel_ratio": travel_ratio
            })
    
    return {
        "feasible": len(violations) == 0,
        "violations": violations,
        "score": 1.0 - (len(violations) / 10.0)  # max 10 violations
    }
```

---

### 4.2 Edit Correctness Evaluation

**Tasks:**
- [ ] **Implement Edit Correctness Eval**
  - Compare original vs edited itinerary
  - Check only intended sections modified
  - Identify unexpected changes
  - Return correctness score
- [ ] **Integration**
  - Run after each edit
  - Hard block if unexpected changes
  - Log results

**Deliverable:** Working edit correctness evaluation

**Files to Create:**
```
backend/
  evaluations/
    edit_correctness_eval.py
```

**Implementation:**
```python
# edit_correctness_eval.py
def evaluate_edit_correctness(original, edited, edit_intent):
    # Parse expected scope from edit intent
    expected_scope = parse_edit_scope(edit_intent)
    # e.g., ["Day 2"] or ["Day 1", "evening"]
    
    # Compute diff
    diff = compute_itinerary_diff(original, edited)
    
    # Check if changes match expected scope
    unexpected = []
    for change in diff.changes:
        if not is_in_scope(change.section, expected_scope):
            unexpected.append(change)
    
    return {
        "correct": len(unexpected) == 0,
        "unexpected_changes": unexpected,
        "expected_scope": expected_scope,
        "actual_changes": diff.changes
    }
```

---

### 4.3 Grounding & Hallucination Evaluation

**Tasks:**
- [ ] **Implement Grounding Eval**
  - Check all POIs have OSM IDs
  - Validate POI IDs exist in dataset
  - Check all explanations have citations
  - Validate citations exist
  - Check missing data explicitly stated
- [ ] **Integration**
  - Run before returning to user
  - Hard block if hallucinations found
  - Log results

**Deliverable:** Working grounding evaluation

**Files to Create:**
```
backend/
  evaluations/
    grounding_eval.py
```

**Implementation:**
```python
# grounding_eval.py
def evaluate_grounding(itinerary, explanations, poi_dataset):
    violations = []
    
    # Check POI existence
    for day in itinerary.days:
        for block in day.blocks:
            for poi in block.pois:
                if poi.id not in poi_dataset:
                    violations.append({
                        "type": "poi_not_in_dataset",
                        "poi": poi.name,
                        "poi_id": poi.id
                    })
    
    # Check citations
    for explanation in explanations:
        if not explanation.citations:
            violations.append({
                "type": "missing_citation",
                "explanation": explanation.text[:50]
            })
        else:
            # Validate citations exist
            for citation in explanation.citations:
                if not validate_citation(citation):
                    violations.append({
                        "type": "invalid_citation",
                        "citation": citation
                    })
    
    return {
        "grounded": len(violations) == 0,
        "violations": violations
    }
```

---

### 4.4 Evaluation Integration

**Tasks:**
- [ ] **Pre-Response Validation**
  - Run all 3 evals before returning to user
  - Hard block on failures
  - Return errors with explanations
- [ ] **Eval Logging**
  - Log all eval results
  - Create eval dashboard (optional, for demo)
  - Export eval results for documentation

**Deliverable:** Integrated evaluation system

**Files to Create:**
```
backend/
  evaluations/
    eval_orchestrator.py
    eval_logger.py
```

---

## Phase 5: UI & Output Generation (Week 6-7)

### 5.1 Companion UI

**Tasks:**
- [ ] **Day-wise Itinerary Display**
  - Show Day 1, Day 2, Day 3
  - Morning/Afternoon/Evening blocks
  - POI names and descriptions
- [ ] **Duration & Travel Time**
  - Show duration for each block
  - Show travel time between stops
  - Visual indicators (optional)
- [ ] **Microphone Button & Live Transcript**
  - Integrate with voice interface
  - Show live transcript as user speaks
  - Show system responses
- [ ] **Sources/References Section**
  - Display citations for each POI
  - Display citations for explanations
  - Link to source URLs
- [ ] **UI Framework**
  - Use Lovable or build with React/Next.js
  - Make it responsive
  - Keep it simple but functional

**Deliverable:** Complete UI with all required elements

**Files to Create:**
```
frontend/
  components/
    ItineraryDisplay.tsx
    DayBlock.tsx
    SourcesSection.tsx
    MicrophoneButton.tsx
    LiveTranscript.tsx
  pages/
    Home.tsx
```

---

### 5.2 PDF Generation

**Tasks:**
- [ ] **PDF Itinerary Generator**
  - Create PDF template
  - Include day-wise itinerary
  - Include time blocks
  - Include POI details
  - Include sources/citations
- [ ] **PDF Library**
  - Use libraries like `pdfkit` (Node.js) or `reportlab` (Python)
  - Or use HTML-to-PDF conversion

**Deliverable:** PDF generation working

**Files to Create:**
```
backend/
  output/
    pdf_generator.py (or .js)
```

---

### 5.3 n8n Email Integration

**Tasks:**
- [ ] **Set up n8n Workflow**
  - Create workflow to receive itinerary data
  - Generate PDF (or use backend-generated PDF)
  - Send email with PDF attachment
- [ ] **Backend Integration**
  - Create API endpoint for n8n webhook
  - Send itinerary data to n8n
  - Handle email sending

**Deliverable:** Email integration via n8n

**Files to Create:**
```
backend/
  output/
    n8n_integration.py (or .js)
```

---

## Phase 6: Testing & Deployment (Week 7-8)

### 6.1 Testing

**Tasks:**
- [ ] **Unit Tests**
  - Test feasibility engine
  - Test edit scoping
  - Test evaluations
- [ ] **Integration Tests**
  - Test planning pipeline
  - Test edit flow
  - Test MCP tool calls
- [ ] **End-to-End Tests**
  - Test full planning flow
  - Test edit flow
  - Test explanation generation
- [ ] **Eval Tests**
  - Test all 3 evaluations
  - Verify they catch violations
  - Test with sample data

**Deliverable:** Comprehensive test suite

---

### 6.2 Sample Test Transcripts

**Tasks:**
- [ ] **Create Test Scenarios**
  - Planning scenario: "Plan a 3-day trip to Jaipur..."
  - Edit scenario: "Make Day 2 more relaxed"
  - Explanation scenario: "Why did you pick this place?"
- [ ] **Document Test Transcripts**
  - Save in `test_transcripts/` folder
  - Include expected outputs
  - Include eval results

**Deliverable:** Test transcripts for documentation

**Files to Create:**
```
test_transcripts/
  planning_scenario.txt
  edit_scenario.txt
  explanation_scenario.txt
```

---

### 6.3 Deployment

**Tasks:**
- [ ] **Backend Deployment**
  - Deploy to Vercel, Railway, or Render
  - Set up environment variables
  - Configure API endpoints
- [ ] **Frontend Deployment**
  - Deploy to Vercel, Netlify, or similar
  - Connect to backend API
  - Test deployed version
- [ ] **Get Public URL**
  - Ensure system is accessible
  - Test all features work
  - Document deployment URL

**Deliverable:** Deployed prototype with public URL

---

### 6.4 Documentation

**Tasks:**
- [ ] **README Updates**
  - Architecture overview
  - Setup instructions
  - List of MCP tools used
  - Datasets referenced
  - How to run evals
  - Sample test transcripts
- [ ] **Code Documentation**
  - Document key functions
  - Document MCP tool schemas
  - Document evaluation criteria

**Deliverable:** Complete documentation

---

### 6.5 Demo Video Preparation

**Tasks:**
- [ ] **Plan Demo Script**
  - Voice-based planning (2 min)
  - Voice-based edit (1 min)
  - Explanation ("why this plan?") (1 min)
  - Sources view (30 sec)
  - Show eval running (30 sec)
- [ ] **Prepare Demo Environment**
  - Test all features work
  - Have sample data ready
  - Prepare eval logs to show
- [ ] **Record Demo**
  - Record 5-minute demo
  - Show all required features
  - Show MCP tool calls (logs or UI)
  - Show eval results

**Deliverable:** 5-minute demo video

---

## Implementation Checklist

### Must-Have Features

- [ ] Voice input/output (STT/TTS)
- [ ] Max 6 clarification questions (enforced)
- [ ] Constraint confirmation before planning
- [ ] Voice-based editing with partial regeneration
- [ ] Explanations with citations
- [ ] At least 2 MCP tools (POI Search, Itinerary Builder)
- [ ] RAG integration with citations
- [ ] 3 evaluation types (Feasibility, Edit Correctness, Grounding)
- [ ] PDF generation
- [ ] n8n email integration
- [ ] Deployed prototype (public URL)
- [ ] Git repository with README

### UI Requirements

- [ ] Day-wise itinerary display
- [ ] Morning/Afternoon/Evening blocks
- [ ] Duration and travel time estimates
- [ ] Microphone button
- [ ] Live transcript
- [ ] Sources/References section

### Data Requirements

- [ ] OpenStreetMap integration (POIs)
- [ ] Wikivoyage/Wikipedia integration (RAG)
- [ ] POI IDs mapped to dataset records
- [ ] Missing data explicitly acknowledged

### Demo Video Requirements

- [ ] Voice-based planning demonstration
- [ ] Voice-based edit demonstration
- [ ] Explanation ("why this plan?")
- [ ] Sources view
- [ ] At least one eval running (show in logs or UI)

---

## Timeline Summary

**6-8 Week Timeline (Recommended):**
- **Week 1-2:** Foundation & Infrastructure
- **Week 3-4:** Core Planning System
- **Week 5:** Edit System & Explanations
- **Week 5-6:** Evaluation System
- **Week 6-7:** UI & Output Generation
- **Week 7-8:** Testing & Deployment

**4-5 Week Timeline (Accelerated):**
- **Week 1:** Foundation + Core Planning (basic)
- **Week 2:** Edit System + Explanations
- **Week 3:** Evaluations + UI
- **Week 4:** Testing + Deployment
- **Week 5:** Polish + Demo

---

## Key Success Factors

1. **Start with Evaluations Early:** Build evals in parallel with main system
2. **Test Edit Correctness Extensively:** This is a critical requirement
3. **Make MCP Tool Calls Visible:** Log everything for demo
4. **Focus on One City:** Don't try to support multiple cities
5. **Keep UI Simple:** Functional is better than fancy
6. **Document Everything:** README, code comments, test transcripts

---

## Risk Mitigation

1. **MCP Tool Failures:** Implement fallbacks and error handling
2. **Edit Scoping Issues:** Test extensively, use symbolic validation
3. **RAG Hallucinations:** Enforce citations strictly, validate sources
4. **Voice Quality:** Test with different accents, handle errors gracefully
5. **Deployment Issues:** Test deployment early, have backup plan

---

## Next Steps

1. **Choose Tech Stack:** Decide on Python vs Node.js, voice API, vector DB
2. **Set Up Repository:** Initialize git, create project structure
3. **Start Phase 1:** Begin with foundation and infrastructure
4. **Build Incrementally:** Test each phase before moving to next
5. **Document as You Go:** Don't leave documentation to the end

---

**Good luck with your capstone project!**
