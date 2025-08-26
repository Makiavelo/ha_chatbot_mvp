import pytest
from unittest.mock import Mock, patch
import requests
from src.integration import PharmacyAPIIntegration

class TestPharmacyAPIIntegration:
    
    def setup_method(self):
        self.api = PharmacyAPIIntegration("http://test-api.com/pharmacies")
        
    @patch('src.integration.requests.get')
    def test_get_pharmacy_by_phone_found(self, mock_get):
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "name": "Test Pharmacy",
                "phone": "555-123-4567",
                "city": "Test City",
                "rx_volume": "1000/month"
            },
            {
                "id": "2", 
                "name": "Another Pharmacy",
                "phone": "555-987-6543",
                "city": "Another City",
                "rx_volume": "500/month"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.api.get_pharmacy_by_phone("555-123-4567")
        
        assert result is not None
        assert result["name"] == "Test Pharmacy"
        assert result["phone"] == "555-123-4567"
        assert result["city"] == "Test City"
        mock_get.assert_called_once_with("http://test-api.com/pharmacies", timeout=10)
        
    @patch('src.integration.requests.get')  
    def test_get_pharmacy_by_phone_not_found(self, mock_get):
        # Mock API response with no matching pharmacy
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "name": "Test Pharmacy", 
                "phone": "555-123-4567",
                "city": "Test City"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.api.get_pharmacy_by_phone("555-999-9999")
        
        assert result is None
        
    @patch('src.integration.requests.get')
    def test_get_pharmacy_by_phone_api_error(self, mock_get):
        # Mock API request exception
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        result = self.api.get_pharmacy_by_phone("555-123-4567")
        
        assert result is None
        
    @patch('src.integration.requests.get')
    def test_get_pharmacy_by_phone_timeout(self, mock_get):
        # Mock timeout exception
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        result = self.api.get_pharmacy_by_phone("555-123-4567")
        
        assert result is None
        
    @patch('src.integration.requests.get')
    def test_get_all_pharmacies_success(self, mock_get):
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": "1", "name": "Pharmacy 1"},
            {"id": "2", "name": "Pharmacy 2"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.api.get_all_pharmacies()
        
        assert len(result) == 2
        assert result[0]["name"] == "Pharmacy 1"
        assert result[1]["name"] == "Pharmacy 2"
        
    @patch('src.integration.requests.get')
    def test_get_all_pharmacies_error(self, mock_get):
        # Mock API error
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        result = self.api.get_all_pharmacies()
        
        assert result == []