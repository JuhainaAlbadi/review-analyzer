from database import SessionLocal, engine
from models import Base, Product, Review

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    
    db.query(Review).delete()
    db.query(Product).delete()
    db.commit()

    products = [
    Product(name="Samsung Galaxy S24", category="Phones",
            description="Latest Samsung flagship phone",
            image_url="https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400"),
    Product(name="Sony WH-1000XM5", category="Headphones",
            description="Noise cancelling wireless headphones",
            image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"),
    Product(name="Apple MacBook Air M3", category="Laptops",
            description="Thin and light laptop with M3 chip",
            image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"),
]
    db.add_all(products)
    db.commit()

    reviews = [
        Review(product_id=products[0].id, author="Ahmed", rating=5,
               body="Absolutely love this phone! Camera is incredible and battery lasts all day."),
        Review(product_id=products[0].id, author="Sara", rating=4,
               body="Great phone overall but it gets a bit warm during gaming sessions."),
        Review(product_id=products[0].id, author="Khalid", rating=3,
               body="Decent phone but overpriced for what it offers compared to competitors."),
        Review(product_id=products[0].id, author="Mona", rating=5,
               body="Best Android phone I have ever used. Display is stunning."),

        Review(product_id=products[1].id, author="Yousef", rating=5,
               body="These headphones are a game changer. Noise cancellation is perfect on flights."),
        Review(product_id=products[1].id, author="Fatima", rating=4,
               body="Sound quality is excellent but the ear cushions get uncomfortable after 3 hours."),
        Review(product_id=products[1].id, author="Omar", rating=5,
               body="Worth every penny. Call quality is crystal clear and battery life is amazing."),

        Review(product_id=products[2].id, author="Layla", rating=5,
               body="This laptop is incredibly fast and silent. Perfect for university work."),
        Review(product_id=products[2].id, author="Tariq", rating=4,
               body="Fantastic performance but only two USB-C ports is frustrating."),
        Review(product_id=products[2].id, author="Noor", rating=5,
               body="Lightweight and powerful. The battery easily lasts 12 hours of real use."),
    ]
    db.add_all(reviews)
    db.commit()
    db.close()

    print("✅ Seeded: 3 products, 10 reviews")

if __name__ == "__main__":
    seed()