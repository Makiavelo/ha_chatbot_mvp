import pytest
from src.prompts import (
    get_system_prompt,
    get_returning_customer_prompt, 
    get_new_customer_prompt,
    get_volume_discussion_prompt
)

class TestPrompts:
    
    def test_get_system_prompt(self):
        prompt = get_system_prompt()
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100  # Should be substantial
        assert "Pharmesol" in prompt
        assert "pharmacy" in prompt.lower()
        assert "high" in prompt.lower() and "volume" in prompt.lower()
        
    def test_get_returning_customer_prompt(self):
        pharmacy_data = {
            "name": "Test Pharmacy",
            "city": "Test City", 
            "rx_volume": "1500/day",
            "phone": "555-123-4567",
            "address": "123 Test St"
        }
        
        prompt = get_returning_customer_prompt(pharmacy_data)
        
        assert "Test Pharmacy" in prompt
        assert "Test City" in prompt
        assert "1500/day" in prompt
        assert "555-123-4567" in prompt
        assert "greet them by name" in prompt.lower()
        
    def test_get_returning_customer_prompt_missing_data(self):
        # Test with minimal data
        pharmacy_data = {
            "name": "Minimal Pharmacy"
        }
        
        prompt = get_returning_customer_prompt(pharmacy_data)
        
        assert "Minimal Pharmacy" in prompt
        assert "your location" in prompt  # Default value
        assert "your current volume" in prompt  # Default value
        assert "N/A" in prompt  # For missing phone/address
        
    def test_get_new_customer_prompt(self):
        prompt = get_new_customer_prompt()
        
        assert isinstance(prompt, str)
        assert "new caller" in prompt.lower()
        assert "welcome" in prompt.lower()
        assert "name, location, rx volume" in prompt.lower()
        assert "challenges" in prompt.lower()
        
    def test_get_volume_discussion_prompt_with_volume(self):
        prompt = get_volume_discussion_prompt("2000/day")
        
        assert "2000/day" in prompt
        assert "prescription volume" in prompt.lower()
        assert "trending" in prompt.lower()
        assert "challenges" in prompt.lower()
        
    def test_get_volume_discussion_prompt_no_volume(self):
        prompt = get_volume_discussion_prompt()
        
        assert "prescription volume" in prompt.lower()
        assert "trending" in prompt.lower() 
        assert "pain points" in prompt.lower()
        # Should not contain volume-specific text when no volume provided
        assert "with your current volume" not in prompt