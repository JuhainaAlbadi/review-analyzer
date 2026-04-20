from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Product, Review
from schemas import ProductCreate, ProductOut, ProductSummaryOut, ReviewOut, ChatRequest, ChatResponse
import ai_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    results = (
        db.query(Product, func.avg(Review.rating).label("avg_rating"))
        .outerjoin(Review, Review.product_id == Product.id)
        .group_by(Product.id)
        .all()
    )
    products = []
    for product, avg in results:
        product.avg_rating = round(avg, 1) if avg else None
        products.append(product)
    return products


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}/reviews", response_model=list[ReviewOut])
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db),
    sentiment: str | None = None,
    rating: int | None = None
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    query = db.query(Review).filter(Review.product_id == product_id)

    if rating is not None:
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=422, detail="Rating must be between 1 and 5")
        query = query.filter(Review.rating == rating)

    if sentiment is not None:
        if sentiment not in ("positive", "neutral", "negative"):
            raise HTTPException(status_code=422, detail="Sentiment must be positive, neutral, or negative")
        from models import Analysis
        query = query.join(Analysis, Analysis.review_id == Review.id)\
                     .filter(Analysis.sentiment == sentiment)

    return query.all()


@router.get("/{product_id}/summary", response_model=ProductSummaryOut)
def get_product_summary(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = [{"rating": r.rating, "body": r.body} for r in product.reviews]
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this product")

    try:
        result = ai_service.summarize_product(product.name, reviews)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return result



@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest, db: Session = Depends(get_db)):
    results = (
        db.query(Product, func.avg(Review.rating).label("avg_rating"))
        .outerjoin(Review, Review.product_id == Product.id)
        .group_by(Product.id)
        .all()
    )
    products = [
        {"name": p.name, "category": p.category, "avg_rating": round(avg, 1) if avg else None}
        for p, avg in results
    ]
    try:
        reply = ai_service.chat_recommendation(data.message, products)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return {"reply": reply}



@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    from models import Analysis
    
    total_products = db.query(Product).count()
    total_reviews = db.query(Review).count()
    total_analyses = db.query(Analysis).count()
    
    positive = db.query(Analysis).filter(Analysis.sentiment == "positive").count()
    neutral = db.query(Analysis).filter(Analysis.sentiment == "neutral").count()
    negative = db.query(Analysis).filter(Analysis.sentiment == "negative").count()
    
    top_products = (
        db.query(Product.name, func.avg(Review.rating).label("avg"))
        .join(Review, Review.product_id == Product.id)
        .group_by(Product.id)
        .order_by(func.avg(Review.rating).desc())
        .limit(3)
        .all()
    )
    
    return {
        "total_products": total_products,
        "total_reviews": total_reviews,
        "total_analyses": total_analyses,
        "sentiment": {
            "positive": positive,
            "neutral": neutral,
            "negative": negative
        },
        "top_products": [{"name": p, "avg_rating": round(avg, 1)} for p, avg in top_products]
    }