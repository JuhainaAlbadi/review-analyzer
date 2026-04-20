# AI Review Analyzer

A full-stack web application for managing products and reviews, powered by the Anthropic Claude API. Users can browse products, submit reviews, and get AI-driven sentiment analysis, product summaries, and smart chat recommendations — all from a clean single-page UI.

---

## Features

- **Product Management** — Add, browse, and search products by name or category
- **Review Submission** — Submit reviews with star ratings and validation
- **AI Review Analysis** — Claude analyzes each review for sentiment, key themes, confidence score, and a written summary
- **AI Product Summary** — Aggregates all reviews into pros, cons, and improvement suggestions
- **Sentiment Filtering** — Filter reviews by sentiment (positive / neutral / negative) and star rating
- **AI Chat Assistant** — Floating robot chat widget powered by Claude for product recommendations
- **Statistics Dashboard** — Overview of total products, reviews, analyses, and sentiment breakdown
- **Export to PDF** — Download any analyzed review as a formatted PDF report
- **Dark Mode** — Full dark theme support

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, SQLAlchemy, Alembic |
| AI | Anthropic Claude API (`claude-haiku-4-5`, `claude-opus-4-1`) |
| Database | SQLite |
| Frontend | Vanilla HTML / CSS / JavaScript, jsPDF |

---

## Project Structure

```
review-analyzer/
├── backend/
│   ├── main.py           # FastAPI app entry point + CORS + rate limiting
│   ├── database.py       # SQLAlchemy engine and session
│   ├── models.py         # ORM models: Product, Review, Analysis
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── ai_service.py     # All Claude API calls (analyze, summarize, chat)
│   ├── seed.py           # Sample data loader
│   ├── routers/
│   │   ├── products.py   # /products endpoints + chat + stats
│   │   └── reviews.py    # /reviews endpoints
│   └── prompts/
│       └── analysis.txt  # Claude system prompt
└── frontend/
    └── index.html        # Full single-page UI 
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd review-analyzer
```

### 2. Create virtual environment and install dependencies

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `backend/` folder:

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxx
```

> Never commit `.env` to version control.

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. (Optional) Seed sample data

```bash
python seed.py
```

Inserts 2 sample products and 5 reviews.

### 6. Start the backend server

```bash
uvicorn main:app --reload
```

API runs at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### 7. Open the frontend

Open `frontend/index.html` directly in your browser — no build step required.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List all products with average rating |
| POST | `/products/` | Create a new product |
| GET | `/products/{id}/reviews` | Get reviews (supports `?sentiment=` and `?rating=` filters) |
| GET | `/products/{id}/summary` | AI-generated product summary |
| GET | `/products/stats` | Dashboard stats (counts, sentiment breakdown, top products) |
| POST | `/products/chat` | AI chat recommendation based on current products |
| POST | `/reviews/` | Submit a new review |
| POST | `/reviews/{id}/analyze` | Run AI analysis on a review |
| GET | `/reviews/{id}/analysis` | Retrieve stored analysis result |

---

## Notes

- Analysis results are cached in the database — re-analyzing requires `?force=true`
- The chat assistant responds in the same language the user writes in
- PDF export happens entirely in the browser (no server involved)
