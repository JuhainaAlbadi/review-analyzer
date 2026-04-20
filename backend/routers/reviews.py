from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import Review, Analysis
from schemas import ReviewCreate, ReviewOut, AnalysisOut
from slowapi import Limiter
from slowapi.util import get_remote_address
import ai_service

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/reviews", tags=["reviews"])

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewOut, status_code=201)
def create_review(data: ReviewCreate, db: Session = Depends(get_db)):
    review = Review(**data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.post("/{review_id}/analyze", response_model=AnalysisOut)
@limiter.limit("5/minute")
def analyze_review(request: Request, review_id: int, force: bool = False, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    
    existing = db.query(Analysis).filter(Analysis.review_id == review_id).first()
    if existing and not force:
        return existing

    try:
        result = ai_service.analyze_review(review.rating, review.body)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    if existing:
        for key, val in result.items():
            setattr(existing, key, val)
        db.commit()
        db.refresh(existing)
        return existing

    analysis = Analysis(review_id=review_id, **result)
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/{review_id}/analysis", response_model=AnalysisOut)
def get_analysis(review_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.review_id == review_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this review")
    return analysis

@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # يحذف الـ analysis المرتبطة تلقائياً
    db.query(Analysis).filter(Analysis.review_id == review_id).delete()
    db.delete(review)
    db.commit()