"""
Main entry point for the Pharmesol inbound sales chatbot.
"""
import logging
import sys
from src.chatbot import PharmacyChatbot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def simulate_call():
    """Simulate an inbound call from a pharmacy."""
    print("=" * 60)
    print("🏥 PHARMESOL INBOUND SALES CHATBOT SIMULATION")
    print("=" * 60)
    
    try:
        chatbot = PharmacyChatbot()
        
        # Get mock phone number from user
        print("\nEnter a phone number to simulate an incoming call:")
        print("Tip: Try '555-0001' for a returning customer demo")
        print("Or any other number for a new customer demo")
        
        phone_number = input("Phone number: ").strip()
        if not phone_number:
            phone_number = "555-0001"  # Default for demo
            
        print(f"\n📞 Incoming call from: {phone_number}")
        print("-" * 40)
        
        # Start the call
        initial_response = chatbot.start_call(phone_number)
        print(f"🤖 Bot: {initial_response}")
        
        # Continue conversation loop
        while True:
            print("\n" + "-" * 40)
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 Bot: Thank you for calling Pharmesol! Have a great day!")
                break
                
            if not user_input:
                continue
                
            response = chatbot.continue_conversation(user_input)
            print(f"🤖 Bot: {response}")
            
        # End call and show summary
        print("\n" + "=" * 60)
        print("📊 CALL SUMMARY")
        print("=" * 60)
        
        summary = chatbot.end_call()
        
        print(f"📞 Caller Phone: {phone_number}")
        if summary['pharmacy_info']:
            print(f"🏥 Pharmacy: {summary['pharmacy_info'].get('name', 'N/A')}")
            print(f"📍 Location: {summary['pharmacy_info'].get('city', 'N/A')}")
            print(f"💊 Rx Volume: {summary['pharmacy_info'].get('rx_volume', 'N/A')}")
        else:
            print("🏥 Pharmacy: New customer (not in system)")
            
        print(f"🎯 Customer Type: {summary['conversation_state']}")
        
        func_summary = summary['function_summary']
        print(f"📧 Emails Sent: {func_summary['emails_sent']}")
        print(f"📞 Callbacks Scheduled: {func_summary['callbacks_scheduled']}")
        print(f"📝 New Leads Collected: {func_summary['leads_collected']}")
        
        if func_summary['details']['emails']:
            print("\n📧 Email Details:")
            for email in func_summary['details']['emails']:
                print(f"  • To: {email['to']}")
                print(f"    Subject: {email['subject']}")
                
        if func_summary['details']['callbacks']:
            print("\n📞 Callback Details:")
            for callback in func_summary['details']['callbacks']:
                print(f"  • Phone: {callback['phone']}")
                print(f"    Time: {callback['preferred_time']}")
                
        if func_summary['details']['leads']:
            print("\n📝 Lead Details:")
            for lead in func_summary['details']['leads']:
                print(f"  • Name: {lead['name']}")
                print(f"    Phone: {lead['phone']}")
                print(f"    Email: {lead.get('email', 'N/A')}")
        
    except Exception as e:
        logger.error(f"Error in chatbot simulation: {e}")
        print(f"❌ Error: {e}")
        print("Make sure you have set up your .env file with OPENAI_API_KEY")
        return 1
        
    return 0

def main():
    """Main function to run the chatbot simulation."""
    print("Welcome to the Pharmesol Chatbot Assessment!")
    print("\nThis chatbot simulates inbound calls from pharmacies.")
    print("It can recognize returning customers and collect info from new ones.")
    print("Type 'quit', 'exit', 'bye', or 'goodbye' to end the conversation.\n")
    
    try:
        return simulate_call()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return 0

if __name__ == "__main__":
    sys.exit(main())