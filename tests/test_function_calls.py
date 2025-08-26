import pytest
from src.function_calls import FunctionHandler
from datetime import datetime

class TestFunctionHandler:
    
    def setup_method(self):
        self.handler = FunctionHandler()
        
    def test_send_email(self):
        result = self.handler.execute_function(
            "send_email",
            {
                "email": "test@pharmacy.com",
                "subject": "Follow up from Pharmesol",
                "content": "Thank you for your interest in our services."
            }
        )
        
        assert "Email successfully sent" in result
        assert "test@pharmacy.com" in result
        assert len(self.handler.sent_emails) == 1
        assert self.handler.sent_emails[0]["to"] == "test@pharmacy.com"
        assert self.handler.sent_emails[0]["subject"] == "Follow up from Pharmesol"
        
    def test_schedule_callback(self):
        result = self.handler.execute_function(
            "schedule_callback",
            {
                "phone": "555-123-4567",
                "preferred_time": "tomorrow at 2pm", 
                "notes": "Discuss high-volume solutions"
            }
        )
        
        assert "Callback scheduled" in result
        assert "555-123-4567" in result
        assert len(self.handler.scheduled_callbacks) == 1
        assert self.handler.scheduled_callbacks[0]["phone"] == "555-123-4567"
        assert self.handler.scheduled_callbacks[0]["preferred_time"] == "tomorrow at 2pm"
        
    def test_collect_pharmacy_info(self):
        result = self.handler.execute_function(
            "collect_pharmacy_info",
            {
                "name": "Test Pharmacy",
                "phone": "555-123-4567",
                "email": "contact@testpharmacy.com",
                "city": "Test City",
                "rx_volume": "500/day"
            }
        )
        
        assert "Information for Test Pharmacy" in result
        assert len(self.handler.collected_leads) == 1
        assert self.handler.collected_leads[0]["name"] == "Test Pharmacy"
        assert self.handler.collected_leads[0]["phone"] == "555-123-4567"
        assert self.handler.collected_leads[0]["status"] == "new_lead"
        
    def test_collect_pharmacy_info_minimal(self):
        # Test with only required fields
        result = self.handler.execute_function(
            "collect_pharmacy_info",
            {
                "name": "Minimal Pharmacy",
                "phone": "555-999-9999"
            }
        )
        
        assert "Information for Minimal Pharmacy" in result
        assert len(self.handler.collected_leads) == 1
        assert self.handler.collected_leads[0]["name"] == "Minimal Pharmacy"
        assert self.handler.collected_leads[0]["email"] == ""
        
    def test_unknown_function(self):
        result = self.handler.execute_function("unknown_function", {})
        assert "Unknown function" in result
        
    def test_get_function_definitions(self):
        functions = self.handler.get_function_definitions()
        
        assert len(functions) == 3
        function_names = [f["name"] for f in functions]
        assert "send_email" in function_names
        assert "schedule_callback" in function_names
        assert "collect_pharmacy_info" in function_names
        
    def test_get_summary_empty(self):
        summary = self.handler.get_summary()
        
        assert summary["emails_sent"] == 0
        assert summary["callbacks_scheduled"] == 0  
        assert summary["leads_collected"] == 0
        assert len(summary["details"]["emails"]) == 0
        
    def test_get_summary_with_data(self):
        # Add some test data
        self.handler.execute_function("send_email", {
            "email": "test@test.com",
            "subject": "Test",
            "content": "Test content"
        })
        self.handler.execute_function("schedule_callback", {
            "phone": "555-123-4567",
            "preferred_time": "tomorrow"
        })
        self.handler.execute_function("collect_pharmacy_info", {
            "name": "Test Pharmacy",
            "phone": "555-987-6543"
        })
        
        summary = self.handler.get_summary()
        
        assert summary["emails_sent"] == 1
        assert summary["callbacks_scheduled"] == 1
        assert summary["leads_collected"] == 1
        assert len(summary["details"]["emails"]) == 1
        assert len(summary["details"]["callbacks"]) == 1
        assert len(summary["details"]["leads"]) == 1