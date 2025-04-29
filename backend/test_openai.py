from openai import OpenAI
from dotenv import load_dotenv
import os

def test_openai_connection():
    print("Starting OpenAI API test...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please make sure you have a .env file with OPENAI_API_KEY=your_key_here")
        return False
    
    print("✓ Found API key in environment variables")
    print(f"API Key starts with: {api_key[:6]}...")
    
    try:
        # Initialize the client without any extra parameters
        print("Attempting to initialize OpenAI client...")
        client = OpenAI()
        
        # Try a simple API call
        print("Testing API connection with a simple request...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using 3.5 for testing as it's cheaper
            messages=[{"role": "user", "content": "Say 'API test successful' if you receive this."}],
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        print(f"✓ API Response received: {result}")
        print("\n✅ All tests passed! OpenAI API is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during API test: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check if your API key is valid")
        print("2. Make sure you have billing set up in your OpenAI account")
        print("3. Verify your API key has the necessary permissions")
        return False

if __name__ == "__main__":
    test_openai_connection() 