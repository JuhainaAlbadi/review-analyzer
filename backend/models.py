from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    category    = Column(String(100), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    product_id   = Column(Integer, ForeignKey("products.id"), nullable=False)
    author       = Column(String(100), nullable=False)
    rating       = Column(Integer, nullable=False)
    body         = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    product  = relationship("Product", back_populates="reviews")
    analysis = relationship("Analysis", back_populates="review", uselist=False)


class Analysis(Base):
    __tablename__ = "analyses"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    review_id   = Column(Integer, ForeignKey("reviews.id"), unique=True, nullable=False)
    sentiment   = Column(String(20))
    summary     = Column(Text)
    key_themes  = Column(JSON)
    confidence  = Column(Float)
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("Review", back_populates="analysis")