# API Endpoints Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: (configure in `.env`)

## Endpoints

### 1. Root & Health

#### `GET /`
Get API information and available endpoints.

**Response:**
```json
{
  "message": "Voice-First Travel Planning Assistant API",
  "status": "running",
  "version": "1.0.0",
  "endpoints": {
    "planning": "/api/plan",
    "edit": "/api/edit",
    "explain": "/api/explain",
    "evaluations": "/api/eval/*"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. Planning

#### `POST /api/plan`
Create or continue planning based on user input.

**Request Body:**
```json
{
  "user_input": "Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace."
}
```

**Response:**
```json
{
  "action": "itinerary",
  "itinerary": {
    "days": [...]
  },
  "reasoning": {...},
  "poi_count": 15,
  "message": "Created 3-day itinerary for Jaipur, India!",
  "rag_loaded": true,
  "rag_citations": [...],
  "rag_descriptions": {...}
}
```

**Possible Actions:**
- `"ask"` - Needs clarification (returns `question` field)
- `"itinerary"` - Successfully created itinerary
- `"error"` - Error occurred (returns `message` field)

---

### 3. Itinerary Management

#### `GET /api/itinerary`
Get the current itinerary.

**Response:**
```json
{
  "itinerary": {
    "days": [...]
  },
  "constraints": {...}
}
```

Or if no itinerary:
```json
{
  "itinerary": null,
  "message": "No itinerary created yet"
}
```

#### `POST /api/reset`
Reset the current state (for new planning session).

**Response:**
```json
{
  "message": "State reset successfully"
}
```

---

### 4. Editing

#### `POST /api/edit`
Edit itinerary based on voice command.

**Request Body:**
```json
{
  "edit_command": "Make Day 2 more relaxed"
}
```

**Response:**
```json
{
  "action": "edit_applied",
  "itinerary": {...},
  "changes": [...],
  "message": "Applied pace edit to day 2"
}
```

---

### 5. Explanations

#### `POST /api/explain`
Answer questions about the plan.

**Request Body:**
```json
{
  "question": "Why did you pick Hawa Mahal?"
}
```

**Response:**
```json
{
  "answer": "...",
  "citations": [...],
  "grounded": true
}
```

---

### 6. Evaluations

#### `POST /api/eval/feasibility`
Run feasibility evaluation on current itinerary.

**Response:**
```json
{
  "passed": true,
  "score": 0.85,
  "details": {...}
}
```

#### `POST /api/eval/edit`
Run edit correctness evaluation.

**Request Body:**
```json
{
  "original": {...},
  "edited": {...},
  "edit_request": {...},
  "changes": [...]
}
```

**Response:**
```json
{
  "passed": true,
  "score": 0.9,
  "details": {...}
}
```

#### `POST /api/eval/grounding`
Run grounding evaluation.

**Response:**
```json
{
  "passed": true,
  "score": 0.88,
  "details": {...}
}
```

#### `GET /api/eval/all`
Run all evaluations.

**Response:**
```json
{
  "all_passed": true,
  "average_score": 0.87,
  "results": {
    "feasibility": {...},
    "grounding": {...}
  }
}
```

---

### 7. Email

#### `POST /api/send-email`
Send current itinerary via email.

**Request Body:**
```json
{
  "recipient_emails": ["user@example.com"],
  "subject": "Your Travel Itinerary from Voyage"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully"
}
```

**Note:** Requires email configuration in `.env` file.

---

## Error Responses

All endpoints may return errors in this format:

```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (missing required data)
- `500` - Internal Server Error
- `503` - Service Unavailable (e.g., email not configured)

---

## Testing

Use the provided test script:

```bash
cd backend
python3 test_api.py
```

Or test manually with curl:

```bash
# Health check
curl http://localhost:8000/health

# Create plan
curl -X POST http://localhost:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Plan a 2-day trip to Jaipur"}'
```

---

## CORS

The API has CORS enabled for all origins (development mode). In production, configure allowed origins in `main.py`.
