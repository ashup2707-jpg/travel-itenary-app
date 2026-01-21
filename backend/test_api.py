"""
Quick API endpoint test script
Tests if all endpoints are accessible and working
"""
import requests
import json
import sys

API_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, description="", timeout=None):
    """Test an API endpoint
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        data: Request body data (for POST)
        description: Human-readable description
        timeout: Custom timeout in seconds (defaults based on endpoint)
    """
    # Set appropriate timeouts based on endpoint
    if timeout is None:
        if endpoint == "/api/plan":
            # Planning endpoint needs longest timeout (LLM + RAG + POI search)
            timeout = 180  # 3 minutes
        elif endpoint == "/api/edit" or endpoint == "/api/explain":
            # Edit/explain endpoints use LLM
            timeout = 60  # 1 minute
        elif method == "GET":
            timeout = 10  # 10 seconds for GET requests
        else:
            timeout = 30  # 30 seconds for other POST requests
    
    try:
        url = f"{API_URL}{endpoint}"
        print(f"\n🧪 Testing {description or endpoint}...")
        print(f"   {method.upper()} {url}")
        
        if endpoint == "/api/plan":
            print(f"   ⏱️  Using extended timeout ({timeout}s) for planning endpoint")
        
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        else:
            print(f"   ❌ Unsupported method: {method}")
            return False
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code < 400:
            try:
                result = response.json()
                print(f"   ✅ Success")
                if isinstance(result, dict) and len(str(result)) < 200:
                    print(f"   Response: {json.dumps(result, indent=2)[:150]}...")
                return True
            except:
                print(f"   ✅ Success (non-JSON response)")
                return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            try:
                error = response.json()
                print(f"   Error detail: {error}")
            except:
                print(f"   Error text: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Backend server not running on {API_URL}")
        print(f"   💡 Start the server with: cd backend && python3 main.py")
        return False
    except requests.exceptions.Timeout:
        print(f"   ⚠️  Timeout: Request took longer than {timeout}s")
        if endpoint == "/api/plan":
            print(f"   💡 Planning endpoint can take 60-120s due to:")
            print(f"      - LLM API calls (Groq/OpenAI)")
            print(f"      - RAG data loading and querying")
            print(f"      - POI search from OpenStreetMap")
            print(f"      - Itinerary building and optimization")
            print(f"   💡 Current timeout is {timeout}s. If this persists, check backend logs for errors")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🚀 API Endpoint Test Suite")
    print("=" * 60)
    
    # Test 1: Root endpoint
    test_endpoint("GET", "/", description="Root endpoint")
    
    # Test 2: Health check
    test_endpoint("GET", "/health", description="Health check")
    
    # Test 3: Get current itinerary (should return empty)
    test_endpoint("GET", "/api/itinerary", description="Get current itinerary")
    
    # Test 4: Create a plan (simple request)
    # This endpoint can take 60-120 seconds due to LLM calls, RAG loading, and POI search
    print("\n⏳ Note: Planning endpoint may take 60-120 seconds...")
    test_endpoint(
        "POST", 
        "/api/plan",
        data={"user_input": "Plan a 2-day trip to Jaipur"},
        description="Create plan (LLM + RAG + POI search - may take 60-120s)",
        timeout=180  # 3 minutes for safety
    )
    
    # Test 5: Get itinerary again (should have data now)
    test_endpoint("GET", "/api/itinerary", description="Get itinerary after creation", timeout=15)
    
    # Test 6: Reset state
    test_endpoint("POST", "/api/reset", description="Reset state")
    
    print("\n" + "=" * 60)
    print("✅ API Test Complete!")
    print("=" * 60)
    print("\n💡 Notes:")
    print("   - Some endpoints require an itinerary to be created first")
    print("   - /api/plan typically takes 60-120s due to:")
    print("     • LLM API calls (Groq/OpenAI/Gemini)")
    print("     • RAG data loading and vector search")
    print("     • OpenStreetMap POI queries")
    print("     • Itinerary building and feasibility checks")
    print("   - Timeouts are set to 180s for /api/plan to handle slow responses")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
