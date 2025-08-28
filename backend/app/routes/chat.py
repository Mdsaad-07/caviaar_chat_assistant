from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import Dict, Any
import uuid
from datetime import datetime

from ..database.database import get_session
from ..database.models import ChatMessage, ChatResponse, ChatSession
from ..services.openai_client import openai_client

chat_router = APIRouter()

@chat_router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    message: ChatMessage,
    db_session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Main chat endpoint for AI shopping assistant
    """
    try:
        # Get or create session
        session_id = message.session_id or str(uuid.uuid4())
        chat_session = db_session.query(ChatSession).filter(
            ChatSession.session_id == session_id
        ).first()

        if not chat_session:
            # Create new chat session
            chat_session = ChatSession(
                session_id=session_id,
                messages="[]",
                context="{}"
            )
            db_session.add(chat_session)
            db_session.commit()

        # Get conversation history
        conversation_history = chat_session.get_messages()

        # Generate AI response
        ai_response = await openai_client.generate_response(
            user_message=message.message,
            conversation_history=conversation_history,
            product_context=[]  # TODO: Add product search
        )

        # Add messages to conversation history
        chat_session.add_message("user", message.message, {})
        chat_session.add_message("assistant", ai_response["response"], ai_response.get("metadata"))

        # Update session in database
        db_session.merge(chat_session)
        db_session.commit()

        return ChatResponse(
            response=ai_response["response"],
            session_id=session_id,
            suggested_products=None,  # TODO: Add product suggestions
            metadata=ai_response.get("metadata")
        )

    except Exception as e:
        print(f"❌ Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Sorry, I'm experiencing technical difficulties. Please try again."
        )

@chat_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Chat service is running"}

@chat_router.get("/stats")
async def get_system_stats() -> Dict[str, Any]:
    """Get system statistics"""
    try:
        return {
            "system": "E-commerce AI Shopping Assistant",
            "status": "operational",
            "model": "gpt-4o-mini",
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        print(f"❌ Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")