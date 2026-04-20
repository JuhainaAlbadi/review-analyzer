import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "analysis.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def analyze_review(rating: int, body: str) -> dict:
    system_prompt = load_prompt()

    user_message = f"Analyze this product review:\nRating: {rating}/5\nReview: {body}"

    try:
        response = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        raw = response.content[0].text
        result = json.loads(raw)

        required_keys = {"sentiment", "summary", "key_themes", "confidence"}
        if not required_keys.issubset(result.keys()):
            raise ValueError(f"Missing keys in AI response: {result.keys()}")

        return result

    except anthropic.APITimeoutError:
        raise RuntimeError("AI service timed out. Please try again.")
    except anthropic.APIError as e:
        raise RuntimeError(f"AI service error: {str(e)}")
    except json.JSONDecodeError:
        raise RuntimeError("AI returned invalid JSON.")


def chat_recommendation(message: str, products: list[dict]) -> str:
    products_text = "\n".join([
        f"- {p['name']} (Category: {p.get('category') or 'N/A'}, Avg Rating: {p.get('avg_rating') or 'No ratings'})"
        for p in products
    ])

    system_prompt = (
        "You are a helpful product assistant. You have access to a list of products and their ratings. "
        "Answer the user's question helpfully and concisely based on the available products. "
        "Respond in the same language the user writes in."
    )

    user_message = f"Available products:\n{products_text}\n\nUser question: {message}"

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text

    except anthropic.APITimeoutError:
        raise RuntimeError("AI service timed out. Please try again.")
    except anthropic.APIError as e:
        raise RuntimeError(f"AI service error: {str(e)}")


def summarize_product(product_name: str, reviews: list[dict]) -> dict:
    system_prompt = load_prompt()

    reviews_text = "\n".join([
        f"- Rating: {r['rating']}/5 | Review: {r['body']}"
        for r in reviews
    ])

    user_message = f"Summarize all reviews for product: {product_name}\n\nReviews:\n{reviews_text}"

    try:
        response = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        raw = response.content[0].text
        result = json.loads(raw)

        required_keys = {"overall_sentiment", "top_pros", "top_cons", "recommended_improvements"}
        if not required_keys.issubset(result.keys()):
            raise ValueError(f"Missing keys in AI response: {result.keys()}")

        return result

    except anthropic.APITimeoutError:
        raise RuntimeError("AI service timed out. Please try again.")
    except anthropic.APIError as e:
        raise RuntimeError(f"AI service error: {str(e)}")
    except json.JSONDecodeError:
        raise RuntimeError("AI returned invalid JSON.")