import requests
from typing import Optional, Dict, Any
import logging
from .config import PHARMACY_API_URL

logger = logging.getLogger(__name__)


class PharmacyAPIIntegration:
    def __init__(self, api_url: str = PHARMACY_API_URL):
        self.api_url = api_url

    def get_pharmacy_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """
        Fetch pharmacy data by phone number from the API.

        Args:
            phone_number: The pharmacy's phone number

        Returns:
            Dictionary containing pharmacy data if found, None otherwise
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()

            pharmacies = response.json()

            # Search for pharmacy with matching phone number
            for pharmacy in pharmacies:
                if pharmacy.get("phone") == phone_number:
                    logger.info(f"Found pharmacy: {pharmacy.get('name', 'Unknown')}")
                    return pharmacy

            logger.info(f"No pharmacy found with phone number: {phone_number}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def get_all_pharmacies(self) -> list:
        """
        Fetch all pharmacies from the API.

        Returns:
            List of pharmacy dictionaries
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
