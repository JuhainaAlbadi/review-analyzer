from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ─── Product ───────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    avg_rating: Optional[float] = None

    class Config:
        from_attributes = True

# ─── Review ────────────────────────────────────────

class ReviewCreate(BaseModel):
    product_id: int
    author: str
    rating: int = Field(..., ge=1, le=5)
    body: str = Field(..., min_length=10)

class ReviewOut(BaseModel):
    id: int
    product_id: int
    author: str
    rating: int
    body: str
    submitted_at: datetime

    class Config:
        from_attributes = True

# ─── Analysis ──────────────────────────────────────

class AnalysisOut(BaseModel):
    id: int
    review_id: int
    sentiment: str
    summary: str
    key_themes: list[str]
    confidence: float
    analyzed_at: datetime

    class Config:
        from_attributes = True

# ─── Product Summary (AI) ──────────────────────────

class ProductSummaryOut(BaseModel):
    overall_sentiment: str
    top_pros: list[str]
    top_cons: list[str]
    recommended_improvements: list[str]


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str