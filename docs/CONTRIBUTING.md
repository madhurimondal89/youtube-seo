# Contributing to TubePilot AI

Thank you for your interest in contributing to TubePilot AI! We welcome contributions that maintain our core architectural principles:
1. **Data & Statistics First, AI Second**: Mathematical reproducibility and transparency over LLM hallucinations.
2. **Stateless Core**: No mandatory databases or heavy background queues.
3. **Lawful & Ethical Data Collection**: Polite rate limiting without circumventing CAPTCHAs or private controls.

---

## Development Setup

### Backend (Python 3.11+)
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Run backend tests
python -m pytest

# 3. Start local development server
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend (Next.js 15+ / TypeScript)
```bash
cd frontend
npm install
npm run dev
```

---

## Code Quality Standards
- All new scoring algorithms must be mathematically defined in `docs/SEO_SCORING.md` before coding.
- New endpoints must include automated tests in `backend/tests/`.
- Frontend UI should adhere to the established dark-mode glassmorphic theme and include responsive mobile layouts.
