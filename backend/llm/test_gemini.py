"""
Quick test script to verify Gemini API is working
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from llm.llm_client import LLMClient

def test_gemini():
    """Test Gemini API connection"""
    try:
        print("🔍 Testing Gemini API connection...")
        
        client = LLMClient(provider="gemini")
        print("✅ LLM Client initialized successfully")
        
        # Simple test
        prompt = "Say 'Hello, Gemini is working!' in exactly those words."
        print(f"\n📤 Sending test prompt...")
        
        response = client.call(prompt, temperature=0.7)
        print(f"\n📥 Response received:")
        print(f"   {response}")
        
        print("\n✅ Gemini API is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure GEMINI_API_KEY is set in .env file")
        print("2. Make sure you've installed: pip install google-generativeai")
        print("3. Check your API key is valid at https://makersuite.google.com/app/apikey")
        return False

if __name__ == "__main__":
    success = test_gemini()
    sys.exit(0 if success else 1)
