import pytest
from unittest.mock import Mock, patch
from src.chatbot import PharmacyChatbot

class TestPharmacyChatbot:
    
    def setup_method(self):
        self.chatbot = PharmacyChatbot()
        
    @patch('src.chatbot.PharmacyAPIIntegration')
    @patch('src.chatbot.ChatbotLLM')
    def test_start_call_returning_customer(self, mock_llm_class, mock_api_class):
        # Mock returning customer data
        mock_pharmacy_data = {
            "id": "1",
            "name": "Test Pharmacy", 
            "phone": "555-123-4567",
            "city": "Test City",
            "rx_volume": "1000/month"
        }
        
        mock_api = Mock()
        mock_api.get_pharmacy_by_phone.return_value = mock_pharmacy_data
        mock_api_class.return_value = mock_api
        
        mock_llm = Mock()
        mock_llm.generate_response.return_value = {
            "content": "Hello Test Pharmacy! Great to hear from you again.",
            "function_call": None
        }
        mock_llm_class.return_value = mock_llm
        
        # Recreate chatbot with mocked dependencies
        chatbot = PharmacyChatbot()
        
        result = chatbot.start_call("555-123-4567")
        
        assert "Hello Test Pharmacy" in result
        assert chatbot.conversation_state == "returning_customer"
        assert chatbot.current_pharmacy == mock_pharmacy_data
        mock_api.get_pharmacy_by_phone.assert_called_once_with("555-123-4567")
        
    @patch('src.chatbot.PharmacyAPIIntegration')
    @patch('src.chatbot.ChatbotLLM')  
    def test_start_call_new_customer(self, mock_llm_class, mock_api_class):
        # Mock new customer (no pharmacy found)
        mock_api = Mock()
        mock_api.get_pharmacy_by_phone.return_value = None
        mock_api_class.return_value = mock_api
        
        mock_llm = Mock()
        mock_llm.generate_response.return_value = {
            "content": "Thank you for calling! I'd love to learn about your pharmacy.",
            "function_call": None
        }
        mock_llm_class.return_value = mock_llm
        
        # Recreate chatbot with mocked dependencies
        chatbot = PharmacyChatbot()
        
        result = chatbot.start_call("555-999-9999")
        
        assert "Thank you for calling" in result
        assert chatbot.conversation_state == "new_customer"
        assert chatbot.current_pharmacy is None
        mock_api.get_pharmacy_by_phone.assert_called_once_with("555-999-9999")
        
    @patch('src.chatbot.PharmacyAPIIntegration')
    @patch('src.chatbot.ChatbotLLM')
    @patch('src.chatbot.FunctionHandler')
    def test_continue_conversation_with_function_call(self, mock_handler_class, mock_llm_class, mock_api_class):
        # Setup mocks
        mock_api = Mock()
        mock_api_class.return_value = mock_api
        
        mock_llm = Mock()
        mock_llm.generate_response.return_value = {
            "content": "I'll send you that information right away.",
            "function_call": {
                "name": "send_email",
                "arguments": {
                    "email": "test@pharmacy.com",
                    "subject": "Pharmesol Information", 
                    "content": "Thank you for your interest!"
                }
            }
        }
        mock_llm_class.return_value = mock_llm
        
        mock_handler = Mock()
        mock_handler.execute_function.return_value = "Email sent successfully!"
        mock_handler.get_function_definitions.return_value = []
        mock_handler_class.return_value = mock_handler
        
        # Recreate chatbot with mocked dependencies
        chatbot = PharmacyChatbot()
        
        result = chatbot.continue_conversation("Can you email me more information?")
        
        assert "I'll send you that information" in result
        assert "Email sent successfully" in result
        mock_handler.execute_function.assert_called_once_with("send_email", {
            "email": "test@pharmacy.com",
            "subject": "Pharmesol Information",
            "content": "Thank you for your interest!"
        })
        
    def test_end_call(self):
        # Setup some test state
        self.chatbot.current_pharmacy = {"name": "Test Pharmacy"}
        self.chatbot.conversation_state = "returning_customer"
        
        summary = self.chatbot.end_call()
        
        assert "pharmacy_info" in summary
        assert "conversation_state" in summary
        assert "function_summary" in summary
        # Verify cleanup
        assert self.chatbot.current_pharmacy is None
        assert self.chatbot.conversation_state == "initial"
        
    def test_get_current_context(self):
        # Setup test state
        self.chatbot.current_pharmacy = {"name": "Test Pharmacy"}
        self.chatbot.conversation_state = "returning_customer"
        
        context = self.chatbot.get_current_context()
        
        assert context["current_pharmacy"]["name"] == "Test Pharmacy"
        assert context["conversation_state"] == "returning_customer"
        assert "conversation_history" in context

class TestChatbotIntegration:
    """Integration tests that test multiple components together."""
    
    @patch('src.integration.requests.get')
    def test_full_conversation_flow_returning_customer(self, mock_requests):
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "name": "MegaPharm",
                "phone": "555-123-4567", 
                "city": "New York",
                "rx_volume": "2000/day",
                "address": "123 Main St"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # This test would need OpenAI API key to run fully
        # For now, we'll test the API integration part
        chatbot = PharmacyChatbot()
        
        # Test that the pharmacy is found
        pharmacy = chatbot.api_integration.get_pharmacy_by_phone("555-123-4567")
        assert pharmacy is not None
        assert pharmacy["name"] == "MegaPharm"
        assert pharmacy["rx_volume"] == "2000/day"