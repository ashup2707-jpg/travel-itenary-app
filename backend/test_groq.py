"""
Test Groq API connection and functionality
"""
import os
import sys
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

def test_groq_api():
    """Test if Groq API is working"""
    print("=" * 60)
    print("🧪 Testing Groq API Connection")
    print("=" * 60)
    
    # Check if API key is set
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("   Please set GROQ_API_KEY in your .env file")
        return False
    
    print("✅ GROQ_API_KEY found")
    
    # Check model
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    print(f"📦 Using model: {groq_model}")
    
    # Try to initialize client
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        print("\n🔄 Testing API call...")
        
        # Make a simple test call
        response = client.chat.completions.create(
            model=groq_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, Groq is working!' if you can read this."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Call Successful!")
        print(f"📝 Response: {result}")
        
        # Check response metadata
        if hasattr(response, 'usage'):
            print(f"\n📊 Usage:")
            print(f"   Tokens used: {response.usage.total_tokens}")
            print(f"   Prompt tokens: {response.usage.prompt_tokens}")
            print(f"   Completion tokens: {response.usage.completion_tokens}")
        
        return True
        
    except ImportError:
        print("❌ Error: openai package not installed")
        print("   Run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Error calling Groq API: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Provide helpful error messages
        error_str = str(e).lower()
        if "api key" in error_str or "authentication" in error_str:
            print("   💡 Check if your GROQ_API_KEY is correct")
        elif "rate limit" in error_str:
            print("   💡 You may have hit the rate limit. Try again later.")
        elif "model" in error_str:
            print(f"   💡 Check if model '{groq_model}' is available")
        elif "network" in error_str or "connection" in error_str:
            print("   💡 Check your internet connection")
        
        import traceback
        traceback.print_exc()
        return False

def test_llm_client():
    """Test using the LLMClient wrapper"""
    print("\n" + "=" * 60)
    print("🧪 Testing LLMClient Wrapper")
    print("=" * 60)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from llm.llm_client import LLMClient
        
        print("🔄 Initializing LLMClient...")
        client = LLMClient(provider="groq")
        
        print(f"✅ LLMClient initialized")
        print(f"   Provider: {client.provider}")
        print(f"   Model: {client.model}")
        print(f"   Available providers: {client.available_providers}")
        
        print("\n🔄 Testing LLMClient.call()...")
        result = client.call(
            prompt="Say 'LLMClient is working!' if you can read this.",
            temperature=0.7,
            max_tokens=50
        )
        
        print(f"✅ LLMClient.call() Successful!")
        print(f"📝 Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing LLMClient: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test 1: Direct Groq API
    success1 = test_groq_api()
    
    # Test 2: LLMClient wrapper
    if success1:
        success2 = test_llm_client()
    else:
        print("\n⚠️  Skipping LLMClient test (API key issue)")
        success2 = False
    
    # Summary
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✅ All tests passed! Groq API is working correctly.")
    elif success1:
        print("⚠️  Direct API works, but LLMClient has issues")
    else:
        print("❌ Groq API is not working. Check your configuration.")
    print("=" * 60)
