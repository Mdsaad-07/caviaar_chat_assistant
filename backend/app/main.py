from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from datetime import datetime, timedelta
from collections import defaultdict
import tiktoken

# Load environment variables
load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://caviaarmode.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Token tracking system (use Redis in production)
user_tokens = defaultdict(lambda: {"count": 0, "date": datetime.now().date()})
MAX_TOKENS_PER_DAY = 500

# Initialize tokenizer for counting tokens with fallback for new models
def get_encoding(model_name: str):
    try:
        return tiktoken.encoding_for_model(model_name)
    except KeyError:
        print(f"Warning: No direct mapping for {model_name}. Falling back to cl100k_base.")
        return tiktoken.get_encoding("cl100k_base")

encoding = get_encoding("gpt-4o-mini")

def count_tokens(text: str) -> int:
    """Count tokens in a text string"""
    return len(encoding.encode(text))

def check_and_update_tokens(user_id: str, prompt_tokens: int, response_tokens: int) -> tuple[bool, int]:
    """Check if user is within token limit and update count"""
    today = datetime.now().date()
    
    # Reset count if it's a new day
    if user_tokens[user_id]["date"] != today:
        user_tokens[user_id] = {"count": 0, "date": today}
    
    total_tokens = prompt_tokens + response_tokens
    current_count = user_tokens[user_id]["count"]
    
    if current_count + total_tokens > MAX_TOKENS_PER_DAY:
        return False, current_count
    
    user_tokens[user_id]["count"] += total_tokens
    return True, user_tokens[user_id]["count"]

# Static data for common queries (since no live data yet)
STATIC_DATA = {
    "size_guide": {
        "info": "Here's our comprehensive size guide to help you find the perfect fit:\nShirts & Tops:\nSmall: Chest 34-36\", Waist 28-30\"\nMedium: Chest 38-40\", Waist 32-34\"\nLarge: Chest 42-44\", Waist 36-38\"\nXL: Chest 46-48\", Waist 40-42\"\nTips: For the best fit, make sure to measure yourself while wearing light clothing.",
        "redirect": "https://caviaarmode.com/size-guide"
    },
    "products": {
        "shirts": [
            {
                "name": "Classic White Cotton Shirt",
                "price": "₹2,499",
                "description": "Premium cotton blend, perfect for formal and casual wear",
                "url": "https://caviaarmode.com/products/classic-white-shirt"
            },
            {
                "name": "Striped Casual Shirt",
                "price": "₹2,199",
                "description": "Breathable fabric with modern navy stripes",
                "url": "https://caviaarmode.com/products/striped-casual-shirt"
            },
            {
                "name": "Black Formal Shirt",
                "price": "₹2,799",
                "description": "Elegant black shirt for professional occasions",
                "url": "https://caviaarmode.com/products/black-formal-shirt"
            }
        ],
        "general": "Explore our curated collection of premium shirts designed for modern style and comfort.",
        "redirect": "https://caviaarmode.com/collections/shirts"
    },
    "payments": {
        "methods": ["Credit Card", "Debit Card", "PayPal", "UPI", "Net Banking"],
        "info": "We accept all major payment methods for secure transactions.",
        "redirect": "https://caviaarmode.com/payment-methods"
    },
    "returns": {
        "policy": "Easy 15-day return policy. Items must be unused with original tags.",
        "process": "Contact our support team or initiate return from your account.",
        "redirect": "https://caviaarmode.com/return-policy"
    },
    "shipping": {
        "info": "All orders will be dispatched within 2-3 days of placement. Express delivery: 1-2 business days.",
        "redirect": "https://caviaarmode.com/shipping-policy"
    },
    "offers": {
        "info": "Sign up for our newsletter to get exclusive deals and early access to sales.",
        "redirect": "https://caviaarmode.com"
    },
    "greeting": {
        "info": "Hello! 👋 I’m Caviaar Mode’s shopping assistant. Ask me about our products, sizing, payments, returns or shipping and I’ll be happy to help.",
    }
}

def is_ecommerce_query(user_query: str) -> bool:
    """Check if query is e-commerce related"""
    ecommerce_keywords = [
        "shirt", "product", "clothing", "dress", "pants", "jacket", "shoes", "accessory",
        "size", "fit", "color", "material", "style", "collection", "catalog",
        "buy", "purchase", "price", "cost", "discount", "sale", "offer", "deal",
        "cart", "checkout", "wishlist", "recommend", "suggest",
        "order", "track", "shipping", "delivery", "dispatch", "arrive", "when",
        "status", "cancel", "modify",
        "payment", "pay", "card", "upi", "paypal", "transaction", "refund", "bill",
        "return", "exchange", "replace", "defect", "wrong", "size", "policy",
        "support", "help", "contact", "complaint",
        "account", "profile", "address", "phone", "email", "login", "register",
        "store", "website", "caviaar", "brand", "quality", "review", "rating"
    ]
    
    query_lower = user_query.lower()
    return any(keyword in query_lower for keyword in ecommerce_keywords)

def classify_query(user_query: str) -> str:
    """Classify e-commerce queries"""
    lc = user_query.lower()
    
    # Greetings / small-talk
    if any(word in lc for word in ["hello", "hi", "hey", "good morning",
                                   "good evening", "how are you", "whats up",
                                   "how's it going"]):
        return "greeting"
    
    if not is_ecommerce_query(user_query):
        return "non_ecommerce"
    
    if any(word in lc for word in ["size", "guide", "fit", "measurement"]):
        return "size_guide"
    if any(word in lc for word in ["shirt", "suggest", "recommend", "product", "collection"]):
        return "products"
    if any(word in lc for word in ["payment", "pay", "method", "card", "upi"]):
        return "payments"
    if any(word in lc for word in ["return", "exchange", "refund", "policy"]):
        return "returns"
    if any(word in lc for word in ["shipping", "delivery", "ship", "dispatch"]):
        return "shipping"
    if any(word in lc for word in ["offer", "discount", "deal", "coupon", "sale"]):
        return "offers"
    
    return "general_ecommerce"

def fetch_static_data(query_type: str) -> dict:
    """Fetch relevant static data"""
    if query_type in STATIC_DATA:
        return STATIC_DATA[query_type]
    return {"info": "I can help with questions about products, sizing, payments, returns, or shipping."}

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        if 'query' not in data:
            raise KeyError("Missing 'query' key")
        
        user_query = data['query']
        session_id = data.get('session_id', 'anonymous')
        
    except:
        raise HTTPException(status_code=400, detail="Invalid request")

    # Check if query is e-commerce related
    query_type = classify_query(user_query)
    
    if query_type == "non_ecommerce":
        return {
            "response": "I'm specifically designed to help with Caviaar Mode shopping questions like products, sizing, payments, returns, and shipping. For other topics, please visit our [contact page](https://caviaarmode.com/contact-us).",
            "session_id": session_id,
            "query_type": "non_ecommerce"
        }

    # Count tokens in user query
    prompt_tokens = count_tokens(user_query)
    
    # Check token limit before processing
    if prompt_tokens > MAX_TOKENS_PER_DAY:
        return {
            "response": "I'm sorry, but your query is too long. Please try a shorter question about our products, sizing, or services.",
            "session_id": session_id
        }

    # Get static data
    static_info = fetch_static_data(query_type)

    # Strict e-commerce focused system prompt
    system_prompt = """You are a focused e-commerce assistant for Caviaar Mode fashion website. 

STRICT RULES:
- ONLY answer questions about: products, sizing, payments, returns, shipping, offers, and store policies
- DO NOT provide: coding help, weather info, general knowledge, or any non-shopping topics
- Keep responses under 150 words
- Only include [button links](URL) when specifically relevant to the query
- Be helpful but stay within e-commerce scope
- For product suggestions, use the provided product data

Your expertise: fashion products, sizing guides, payment methods, return policies, shipping info, and customer service."""

    user_prompt = f"Query type: {query_type}\nAvailable info: {json.dumps(static_info)}\nUser question: {user_query}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more focused responses
            max_tokens=150   # Limit response length
        )
        
        bot_reply = response.choices[0].message.content
        response_tokens = count_tokens(bot_reply)
        
        # Check and update token count (internal only, not sent to frontend)
        within_limit, current_count = check_and_update_tokens(session_id, prompt_tokens, response_tokens)
        
        if not within_limit:
            return {
                "response": f"You've reached your daily limit of {MAX_TOKENS_PER_DAY} tokens. Please try again tomorrow or contact support for extended access.",
                "session_id": session_id,
                "query_type": query_type
            }
        
        return {
            "response": bot_reply,
            "session_id": session_id,
            "query_type": query_type
        }
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {
            "response": "I'm having trouble right now. Please visit our [website](https://caviaarmode.com) or [contact support](https://caviaarmode.com/contact) for assistance!",
            "session_id": session_id
        }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "api_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "max_tokens_per_day": MAX_TOKENS_PER_DAY
    }

# Token usage endpoint
@app.get("/api/tokens/{session_id}")
def get_token_usage(session_id: str):
    user_data = user_tokens.get(session_id, {"count": 0, "date": datetime.now().date()})
    return {
        "tokens_used": user_data["count"],
        "tokens_remaining": MAX_TOKENS_PER_DAY - user_data["count"],
        "date": str(user_data["date"])
    }

print("OPENAI_API_KEY:", "Set" if os.getenv("OPENAI_API_KEY") else "Not set")
