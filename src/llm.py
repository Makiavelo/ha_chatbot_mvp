from openai import OpenAI
import json
from typing import Dict, Any, Optional
import logging
from .config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class ChatbotLLM:
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        import httpx

        # Create custom httpx client without proxies
        http_client = httpx.Client(
            trust_env=False  # This disables automatic proxy detection from environment
        )
        self.client = OpenAI(api_key=api_key, http_client=http_client)
        self.model = model
        self.conversation_history = []

    def generate_response(
        self, prompt: str, system_prompt: str, functions: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using OpenAI's API with optional function calling.

        Args:
            prompt: User input or conversation context
            system_prompt: System instructions for the LLM
            functions: Optional list of function definitions for function calling

        Returns:
            Dictionary containing response and any function calls
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                *self.conversation_history,
                {"role": "user", "content": prompt},
            ]

            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500,
            }

            if functions:
                kwargs["tools"] = [
                    {"type": "function", "function": func} for func in functions
                ]
                kwargs["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**kwargs)

            message = response.choices[0].message

            result = {"content": message.content, "function_call": None}

            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_call = message.tool_calls[0]  # Take first tool call
                if tool_call.type == "function":
                    result["function_call"] = {
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments),
                    }

            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            if result["content"]:
                self.conversation_history.append(
                    {"role": "assistant", "content": result["content"]}
                )

            return result

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {
                "content": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
                "function_call": None,
            }

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def add_function_result(self, function_name: str, function_result: str):
        """Add function execution result to conversation history."""
        self.conversation_history.append(
            {"role": "function", "name": function_name, "content": function_result}
        )
