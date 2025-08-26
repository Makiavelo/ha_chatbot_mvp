# Home Assessment Project

## Project Requirements
### Inbound Pharmacy Sales Chatbot (LLM + API Integration)
* Build a simple chatbot simulation that can handle inbound calls from pharmacies who reach out via a phone number listed on our website. The chatbot should be able to intelligently continue the conversation by 
* * Recognize returning pharmacies using caller ID (via phone number lookup).
* * Fetch and reference pharmacy details from an external API.
* * Collect information from new callers if they are not recognized.
* * Enable follow-up actions such as email or callback scheduling (mocked).
* * Showcase how Pharmesol can support high Rx volume pharmacies
* You’re not expected to implement a full voice system. Simulated text-based conversations are fine.
* This task is open ended, feel free to make reasonable assumptions and focus on writing clean, modular code.
* Keep usability and readability in mind, we’re interested in how you organize logic, interact with APIs, and structure chatbot behavior.

### Integration API 
API URL: https://67e14fb758cc6bf785254550.mockapi.io/pharmacies
You'll have access to an external API containing pharmacy data. The bot should check this API to identify whether the caller is an existing pharmacy in our system.
Authentication: No auth required

### Flow requirements
* On "call start," check the caller's phone number against the API. Since we aren’t building end to end calls, you can use a mock variable for the chatbot user’s phone number. 
* * If the pharmacy exists, greet them by name and reference any known data (e.g., location, Rx volume).
* * If unknown, treat them as a new lead and collect basic info conversationally.
* Highlight how your company can support high Rx volume pharmacies by referencing their Rx volume from the API
* Offer to follow up via email or schedule a callback.
* * You can implement mock functions that in the future would be replaced with actual email sending and/or call scheduling (e.g., send_email() or schedule_callback()). They can print that emails/followup scheduled as they won’t actually do them. 
* Handle missing or incomplete data gracefully 

### Test cases
Build test cases to test your LLM output w/ the API integration. Make sure to include a few edge cases as well. 

### Suggestions
Suggestions: 
* Files 
* * prompt.py 
* * function_calls.py
* * llm.py 
* * integration.py 
* * tests.py 

## Important
* Keep usability and readability in mind, we’re interested in how you organize logic, interact with APIs, and structure chatbot behavior.
* Use ENV vars for secrets and data that depends on the environment (like urls, services, etc.)

## Development Setup

### Installation
```bash
pip install -r requirements.txt
```

### Running the Project
```bash
python main.py
```

### Running Tests
```bash
# Add test command when test framework is chosen
# Example: pytest tests/
```

## Project Structure
```
home_assesment/
├── src/              # Source code directory
├── tests/            # Test files
├── main.py           # Main entry point
├── requirements.txt  # Python dependencies
└── CLAUDE.md         # This file
```

## Notes
<!-- Add any additional notes or considerations -->