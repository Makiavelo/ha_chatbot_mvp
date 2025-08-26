import logging
from typing import Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Function definitions for LLM function calling
AVAILABLE_FUNCTIONS = [
    {
        "name": "send_email",
        "description": "Send a follow-up email to a pharmacy",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The pharmacy's email address",
                },
                "subject": {"type": "string", "description": "Email subject line"},
                "content": {"type": "string", "description": "Email content/message"},
            },
            "required": ["email", "subject", "content"],
        },
    },
    {
        "name": "schedule_callback",
        "description": "Schedule a callback for the pharmacy",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "Phone number to call back"},
                "preferred_time": {
                    "type": "string",
                    "description": "Preferred callback time (e.g., 'tomorrow at 2pm', 'next week')",
                },
                "notes": {
                    "type": "string",
                    "description": "Any notes about the callback or what to discuss",
                },
            },
            "required": ["phone", "preferred_time"],
        },
    },
    {
        "name": "collect_pharmacy_info",
        "description": "Collect and store information about a new pharmacy",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Pharmacy name"},
                "phone": {"type": "string", "description": "Pharmacy phone number"},
                "email": {"type": "string", "description": "Pharmacy email address"},
                "address": {"type": "string", "description": "Pharmacy address"},
                "city": {"type": "string", "description": "City location"},
                "rx_volume": {
                    "type": "string",
                    "description": "Current prescription volume (e.g., '500 per day', '3000 per month')",
                },
            },
            "required": ["name", "phone"],
        },
    },
]


class FunctionHandler:
    def __init__(self):
        self.collected_leads = []
        self.scheduled_callbacks = []
        self.sent_emails = []

    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a function call and return the result as a string."""
        if function_name == "send_email":
            return self._send_email(**arguments)
        elif function_name == "schedule_callback":
            return self._schedule_callback(**arguments)
        elif function_name == "collect_pharmacy_info":
            return self._collect_pharmacy_info(**arguments)
        else:
            return f"Unknown function: {function_name}"

    def _send_email(self, email: str, subject: str, content: str) -> str:
        """Mock function to send email."""
        email_record = {
            "to": email,
            "subject": subject,
            "content": content,
            "sent_at": datetime.now().isoformat(),
        }
        self.sent_emails.append(email_record)

        logger.info(f"Email sent to {email} with subject: {subject}")
        return f"Email successfully sent to {email} with subject '{subject}'. The pharmacy will receive our information shortly."

    def _schedule_callback(
        self, phone: str, preferred_time: str, notes: str = ""
    ) -> str:
        """Mock function to schedule a callback."""
        callback_record = {
            "phone": phone,
            "preferred_time": preferred_time,
            "notes": notes,
            "scheduled_at": datetime.now().isoformat(),
            "status": "scheduled",
        }
        self.scheduled_callbacks.append(callback_record)

        logger.info(f"Callback scheduled for {phone} at {preferred_time}")
        return f"Callback scheduled for {phone} at {preferred_time}. Our sales team will reach out to discuss how Pharmesol can support your pharmacy's needs."

    def _collect_pharmacy_info(
        self,
        name: str,
        phone: str,
        email: str = "",
        address: str = "",
        city: str = "",
        rx_volume: str = "",
    ) -> str:
        """Mock function to collect and store new pharmacy information."""
        pharmacy_info = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "city": city,
            "rx_volume": rx_volume,
            "collected_at": datetime.now().isoformat(),
            "status": "new_lead",
        }
        self.collected_leads.append(pharmacy_info)

        logger.info(f"New pharmacy information collected for: {name}")
        return f"Information for {name} has been recorded in our system. We'll use this to better serve your pharmacy's needs."

    def get_function_definitions(self) -> list:
        """Get the function definitions for LLM function calling."""
        return AVAILABLE_FUNCTIONS

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all function executions."""
        return {
            "emails_sent": len(self.sent_emails),
            "callbacks_scheduled": len(self.scheduled_callbacks),
            "leads_collected": len(self.collected_leads),
            "details": {
                "emails": self.sent_emails,
                "callbacks": self.scheduled_callbacks,
                "leads": self.collected_leads,
            },
        }
