import logging
from typing import Dict, Any, Optional
from .integration import PharmacyAPIIntegration
from .llm import ChatbotLLM
from .prompts import (
    get_system_prompt,
    get_returning_customer_prompt,
    get_new_customer_prompt,
    get_volume_discussion_prompt,
)
from .function_calls import FunctionHandler

logger = logging.getLogger(__name__)


class PharmacyChatbot:
    def __init__(self):
        self.api_integration = PharmacyAPIIntegration()
        self.llm = ChatbotLLM()
        self.function_handler = FunctionHandler()
        self.current_pharmacy = None
        self.conversation_state = "initial"

    def start_call(self, caller_phone: str) -> str:
        """
        Initialize a new call session with caller ID lookup.

        Args:
            caller_phone: The phone number of the incoming caller

        Returns:
            Initial greeting message
        """
        logger.info(f"Starting call from phone number: {caller_phone}")

        # Look up pharmacy in the system
        self.current_pharmacy = self.api_integration.get_pharmacy_by_phone(caller_phone)

        if self.current_pharmacy:
            # Returning customer
            logger.info(f"Returning customer: {self.current_pharmacy.get('name')}")
            self.conversation_state = "returning_customer"
            prompt = get_returning_customer_prompt(self.current_pharmacy)
            initial_message = "Thank you for calling Pharmesol! I see you're calling from our records."
        else:
            # New customer
            logger.info("New customer - not found in system")
            self.conversation_state = "new_customer"
            prompt = get_new_customer_prompt()
            initial_message = "Thank you for calling Pharmesol! I don't see your number in our system."

        # Generate initial response
        system_prompt = get_system_prompt()
        response = self.llm.generate_response(
            initial_message,
            system_prompt + "\n\n" + prompt,
            self.function_handler.get_function_definitions(),
        )

        return self._process_response(response)

    def continue_conversation(self, user_input: str) -> str:
        """
        Continue the conversation with user input.

        Args:
            user_input: What the user/caller said

        Returns:
            Bot response
        """
        logger.info(f"User input: {user_input}")

        # Determine appropriate prompt based on conversation state and context
        system_prompt = get_system_prompt()

        if self.conversation_state == "returning_customer" and self.current_pharmacy:
            context_prompt = get_returning_customer_prompt(self.current_pharmacy)
        elif self.conversation_state == "new_customer":
            context_prompt = get_new_customer_prompt()
        else:
            # Default to general conversation
            rx_volume = (
                self.current_pharmacy.get("rx_volume")
                if self.current_pharmacy
                else None
            )
            context_prompt = get_volume_discussion_prompt(rx_volume)

        full_prompt = system_prompt + "\n\n" + context_prompt

        # Generate response
        response = self.llm.generate_response(
            user_input, full_prompt, self.function_handler.get_function_definitions()
        )

        return self._process_response(response)

    def _process_response(self, llm_response: Dict[str, Any]) -> str:
        """
        Process LLM response and handle function calls.

        Args:
            llm_response: Response from LLM including potential function calls

        Returns:
            Final response to show to user
        """
        response_text = llm_response.get("content", "")
        function_call = llm_response.get("function_call")

        if function_call:
            # Execute the function
            function_name = function_call["name"]
            function_args = function_call["arguments"]

            logger.info(
                f"Executing function: {function_name} with args: {function_args}"
            )

            function_result = self.function_handler.execute_function(
                function_name, function_args
            )

            # Add function result to conversation
            self.llm.add_function_result(function_name, function_result)

            # If we collected pharmacy info, update our current pharmacy
            if function_name == "collect_pharmacy_info":
                self.current_pharmacy = function_args
                self.conversation_state = "known_customer"

            # Append function result to response
            if response_text:
                return f"{response_text}\n\n{function_result}"
            else:
                return function_result

        return (
            response_text
            or "I'm here to help with any questions about Pharmesol's services."
        )

    def end_call(self) -> Dict[str, Any]:
        """
        End the call session and return summary.

        Returns:
            Dictionary with call summary and metrics
        """
        summary = {
            "caller_phone": getattr(self, "caller_phone", "Unknown"),
            "pharmacy_info": self.current_pharmacy,
            "conversation_state": self.conversation_state,
            "function_summary": self.function_handler.get_summary(),
        }

        logger.info(f"Call ended. Summary: {summary}")

        # Clear conversation history for next call
        self.llm.clear_history()
        self.current_pharmacy = None
        self.conversation_state = "initial"

        return summary

    def get_current_context(self) -> Dict[str, Any]:
        """Get current conversation context for debugging/monitoring."""
        return {
            "current_pharmacy": self.current_pharmacy,
            "conversation_state": self.conversation_state,
            "conversation_history": self.llm.conversation_history,
        }
