from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, List
from datetime import datetime
import json

class Product(SQLModel, table=True):
    """Product model for storing scraped e-commerce data"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Product name/title")
    description: Optional[str] = Field(default=None, description="Product description")
    price: Optional[float] = Field(default=None, description="Product price")
    currency: Optional[str] = Field(default="USD", description="Price currency")
    category: Optional[str] = Field(default=None, index=True, description="Product category")
    brand: Optional[str] = Field(default=None, index=True, description="Product brand")
    sku: Optional[str] = Field(default=None, unique=True, description="Stock keeping unit")

    # URLs and Images
    url: str = Field(description="Product page URL")
    image_url: Optional[str] = Field(default=None, description="Main product image URL")
    additional_images: Optional[str] = Field(default=None, description="JSON string of additional image URLs")

    # Stock and availability
    in_stock: bool = Field(default=True, description="Product availability")
    stock_quantity: Optional[int] = Field(default=None, description="Available stock quantity")

    # Product attributes (stored as JSON)
    attributes: Optional[str] = Field(default=None, description="JSON string of product attributes (size, color, etc.)")

    # SEO and metadata
    meta_title: Optional[str] = Field(default=None, description="SEO meta title")
    meta_description: Optional[str] = Field(default=None, description="SEO meta description")
    tags: Optional[str] = Field(default=None, description="Comma-separated tags")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update timestamp")
    last_scraped: Optional[datetime] = Field(default=None, description="Last time product was scraped")

    # Rating and reviews
    rating: Optional[float] = Field(default=None, description="Average product rating")
    review_count: Optional[int] = Field(default=None, description="Number of reviews")

    def set_additional_images(self, image_list: List[str]):
        """Set additional images as JSON string"""
        self.additional_images = json.dumps(image_list)

    def get_additional_images(self) -> List[str]:
        """Get additional images from JSON string"""
        if self.additional_images:
            return json.loads(self.additional_images)
        return []

    def set_attributes(self, attr_dict: dict):
        """Set product attributes as JSON string"""
        self.attributes = json.dumps(attr_dict)

    def get_attributes(self) -> dict:
        """Get product attributes from JSON string"""
        if self.attributes:
            return json.loads(self.attributes)
        return {}

class ChatSession(SQLModel, table=True):
    """Chat session model for storing conversation history"""

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True, unique=True, description="Unique session identifier")
    user_id: Optional[str] = Field(default=None, index=True, description="User identifier (if authenticated)")

    # Session data
    messages: str = Field(description="JSON string of conversation messages")
    context: Optional[str] = Field(default=None, description="JSON string of session context")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str, metadata: dict = None):
        """Add a message to the conversation"""
        messages = self.get_messages()
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        messages.append(message)
        self.messages = json.dumps(messages)
        self.last_activity = datetime.utcnow()

    def get_messages(self) -> List[dict]:
        """Get conversation messages"""
        if self.messages:
            return json.loads(self.messages)
        return []

    def set_context(self, context_dict: dict):
        """Set session context"""
        self.context = json.dumps(context_dict)

    def get_context(self) -> dict:
        """Get session context"""
        if self.context:
            return json.loads(self.context)
        return {}

class ProductInteraction(SQLModel, table=True):
    """Track product interactions for analytics and recommendations"""

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True, description="Chat session ID")
    product_id: int = Field(foreign_key="product.id", description="Referenced product ID")

    interaction_type: str = Field(description="Type of interaction (viewed, asked_about, recommended)")
    query: Optional[str] = Field(default=None, description="User query that led to this interaction")

    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Message schemas for API
class ChatMessage(SQLModel):
    """Chat message schema for API requests"""
    message: str = Field(description="User message")
    session_id: Optional[str] = Field(default=None, description="Session ID for conversation continuity")

class ChatResponse(SQLModel):
    """Chat response schema for API responses"""
    response: str = Field(description="AI assistant response")
    session_id: str = Field(description="Session ID")
    suggested_products: Optional[List[dict]] = Field(default=None, description="Suggested products")
    metadata: Optional[dict] = Field(default=None, description="Additional response metadata")