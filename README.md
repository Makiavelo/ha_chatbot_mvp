# Pharmesol Inbound Sales Chatbot

A Python-based chatbot simulation that handles inbound calls from pharmacies, demonstrating intelligent customer recognition, personalized conversations, and automated follow-up actions.

## Features

- 🔍 **Caller ID Recognition**: Automatically identifies returning pharmacies using phone number lookup
- 👤 **Personalized Greetings**: Welcomes returning customers by name with their pharmacy details
- 📝 **Lead Collection**: Conversationally gathers information from new potential customers
- 💊 **High-Volume Focus**: Emphasizes Pharmesol's capabilities for high Rx volume pharmacies
- 📧 **Follow-up Actions**: Email sending and callback scheduling (mocked for demonstration)
- 🧪 **Comprehensive Testing**: Full test suite with edge cases and error scenarios

## Project Structure

```
home_assesment/
├── src/
│   ├── chatbot.py          # Main chatbot orchestration logic
│   ├── integration.py      # Pharmacy API integration
│   ├── llm.py             # OpenAI LLM wrapper
│   ├── prompts.py         # Conversation prompts
│   ├── function_calls.py  # Mock action functions
│   └── config.py          # Environment configuration
├── tests/
│   ├── test_chatbot.py
│   ├── test_integration.py
│   ├── test_function_calls.py
│   └── test_prompts.py
├── main.py               # Interactive simulation entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Setup Instructions

### 1. Clone or Navigate to Project Directory

```bash
cd /path/to/home_assesment
```

### 2. Python Version Management (Optional)

This project includes a `.python-version` file for pyenv compatibility. If you have pyenv installed, it will automatically use Python 3.11.9:

```bash
# Install the required Python version if not already available
pyenv install 3.11.9

# The correct version will be selected automatically when you enter the project directory
cd /path/to/home_assesment
python --version  # Should show Python 3.11.9
```

If you don't have pyenv, ensure you have Python 3.7+ installed.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
```

**Required Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PHARMACY_API_URL`: API endpoint (defaults to provided mock API)
- `OPENAI_MODEL`: OpenAI model to use (defaults to gpt-4o)

### 5. Run the Chatbot Simulation

```bash
python main.py
```

## Usage

### Interactive Simulation

The main script provides an interactive chatbot simulation:

1. **Start the simulation**: `python main.py`
2. **Enter a phone number** when prompted:
   - Try `555-0001` for a returning customer demo
   - Use any other number for a new customer experience
3. **Have a conversation** with the chatbot
4. **Type** `quit`, `exit`, `bye`, or `goodbye` to end the call
5. **View the call summary** with all actions taken

### Testing Different Scenarios

**Returning Customer Flow:**
- Use phone numbers that exist in the pharmacy API
- Bot will greet by pharmacy name and reference known data
- Conversation focuses on existing relationship

**New Customer Flow:**  
- Use phone numbers not in the system
- Bot will collect pharmacy information conversationally
- Emphasizes Pharmesol's high-volume capabilities

**Function Calling Examples:**
- Ask to "send me more information via email"
- Request "schedule a callback for tomorrow"
- Provide pharmacy details during conversation

## Running Tests

Execute the full test suite:

```bash
pytest tests/ -v
```

Run specific test files:

```bash
# Test API integration
pytest tests/test_integration.py -v

# Test chatbot logic
pytest tests/test_chatbot.py -v

# Test function calling
pytest tests/test_function_calls.py -v

# Test prompts
pytest tests/test_prompts.py -v
```

## API Integration

The chatbot integrates with a mock pharmacy API:
- **URL**: `https://67e14fb758cc6bf785254550.mockapi.io/pharmacies`
- **Authentication**: None required
- **Data Format**: JSON array of pharmacy objects

Example pharmacy data structure:
```json
{
  "id": "1",
  "name": "MegaPharm",
  "phone": "555-123-4567",
  "city": "New York",
  "address": "123 Main St",
  "rx_volume": "2000/day"
}
```

## Architecture Overview

### Core Components

1. **PharmacyChatbot** (`chatbot.py`): Main orchestration class
2. **PharmacyAPIIntegration** (`integration.py`): External API client
3. **ChatbotLLM** (`llm.py`): OpenAI API wrapper with conversation management
4. **FunctionHandler** (`function_calls.py`): Mock action execution
5. **Prompts** (`prompts.py`): Context-aware conversation prompts

### Conversation Flow

1. **Call Start**: Phone number lookup in pharmacy database
2. **Context Setting**: Different prompts for returning vs new customers  
3. **Conversation Loop**: LLM generates responses with function calling
4. **Action Execution**: Email, callback, and data collection functions
5. **Call Summary**: Detailed metrics and action tracking

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY environment variable is required"**
- Ensure your `.env` file exists and contains a valid OpenAI API key

**"API request failed"**
- Check internet connection
- Verify the pharmacy API URL is accessible
- Review API timeout settings in `integration.py`

**Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (Python 3.7+)

### Debug Mode

Enable detailed logging by modifying the logging level in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Development Notes

- **Modular Design**: Each component can be tested and modified independently
- **Mock Functions**: All external actions (email, callbacks) are simulated
- **Error Handling**: Graceful degradation when APIs are unavailable
- **Extensible**: Easy to add new function calls and conversation flows

## License

This project is part of a technical assessment.