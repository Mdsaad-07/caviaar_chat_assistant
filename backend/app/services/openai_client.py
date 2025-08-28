import os
from typing import List, Dict, Any
from datetime import datetime
from openai import AsyncOpenAI

class OpenAIClient:
    """OpenAI client wrapper for GPT-4o-mini integration"""
    
    def __init__(self):
        """Initialize OpenAI client with graceful handling for missing key"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 1000))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
        self.system_prompt = "You are a helpful shopping assistant."  # Customizable
        
        if not self.api_key:
            print("⚠️ WARNING: OPENAI_API_KEY not found. Using mock mode.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]] = None,
        product_context: List[Dict] = None
    ) -> Dict[str, Any]:
        if self.client is None:
            # Mock response when no API key
            print("Using mock response due to missing API key.")
            return {
                "response": f"Mock response: I would normally process '{user_message}' with AI, but no API key is set. Here's a placeholder reply!",
                "metadata": {
                    "model": "mock",
                    "tokens_used": {"prompt": 0, "completion": 0, "total": 0},
                    "cost_estimate": 0,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        
        # Build messages for OpenAI
        messages = [{"role": "system", "content": self._build_system_prompt(product_context)}]
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Limit history
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            ai_response = response.choices[0].message.content
            usage = response.usage
            cost_estimate = (usage.prompt_tokens * 0.00000015) + (usage.completion_tokens * 0.0000006)  # gpt-4o-mini pricing
            
            return {
                "response": ai_response,
                "metadata": {
                    "model": self.model,
                    "tokens_used": {"prompt": usage.prompt_tokens, "completion": usage.completion_tokens, "total": usage.total_tokens},
                    "cost_estimate": round(cost_estimate, 6),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        except Exception as e:
            print(f"❌ OpenAI API error: {str(e)}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties right now. Please try again in a moment.",
                "error": str(e),
                "metadata": {
                    "model": self.model,
                    "error_type": type(e).__name__,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
    
    def _build_system_prompt(self, product_context: List[Dict] = None) -> str:
        prompt = self.system_prompt
        if product_context:
            prompt += "\nProduct context:\n" + "\n".join([f"- {p['name']}: {p['description']}" for p in product_context])
        return prompt

# Export the instance
openai_client = OpenAIClient()
