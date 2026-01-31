# Environment setup (.env)

All configuration is in a **`.env`** file at the **project root** (same folder as `backend` and `frontend`). The backend loads it; the frontend only uses `NEXT_PUBLIC_API_URL` if you set it.

---

## Quick setup

1. Copy the template: `cp env.template .env`
2. Edit `.env` and add your keys (no quotes).
3. Restart the backend after changing `.env`.

At repo root you can also copy **PASTE_INTO_DOT_ENV.txt** into `.env` and replace the placeholders.

---

## Variables

### LLM (at least one required for planning)

| Variable | Required | Where to get it |
|----------|----------|------------------|
| **GROQ_API_KEY** | At least one of these | https://console.groq.com/ (free tier) |
| **GEMINI_API_KEY** | | https://makersuite.google.com/app/apikey |
| **OPENAI_API_KEY** | | https://platform.openai.com/api-keys |
| **ANTHROPIC_API_KEY** | | https://console.anthropic.com/ |
| **GROK_API_KEY** or **XAI_API_KEY** | | https://console.x.ai/ |

Optional: `GROQ_MODEL`, `GEMINI_MODEL`, etc. (defaults in code).

### Email (optional — for Share button)

| Variable | Required | Where to get it |
|----------|----------|------------------|
| **SENDER_PASSWORD** | Optional | Gmail App Password: https://myaccount.google.com/apppasswords |
| **SMTP_SERVER** | Optional | Default: smtp.gmail.com |
| **SMTP_PORT** | Optional | Default: 587 |

Sender/receiver emails are hardcoded in code (see email_sender.py).

### Backend

| Variable | Default | Purpose |
|----------|--------|---------|
| **BACKEND_PORT** | 8000 | Port for backend |
| **TARGET_CITY** | Jaipur | Default city if not specified |

### Frontend (optional)

| Variable | Default | Purpose |
|----------|--------|---------|
| **NEXT_PUBLIC_API_URL** | http://localhost:8000 | Backend URL (set in frontend `.env.local` or build env) |

---

## Example minimal `.env` (planning + optional email)

```env
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.1-70b-versatile

SENDER_PASSWORD=your_16_char_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

BACKEND_PORT=8000
TARGET_CITY=Jaipur
```

Do not commit `.env` or share it; it is in `.gitignore`.
