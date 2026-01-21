"""
LLM client supporting Grok (xAI), OpenAI GPT, Google Gemini, Anthropic Claude, and more with fallback
"""
import os
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import time

# Gracefully load .env
try:
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()
except Exception:
    pass  # Continue without .env, rely on environment variables

class LLMClient:
    """
    Unified LLM client that supports Grok (xAI), OpenAI GPT, Google Gemini, Anthropic Claude,
    Groq, and other providers with automatic fallback on rate limits or errors
    """
    
    def __init__(self, provider: str = None, enable_fallback: bool = True):
        """
        Initialize LLM client
        
        Args:
            provider: 'grok', 'openai', 'gemini', 'anthropic', 'groq', or None (auto-detect from env)
            enable_fallback: If True, automatically fallback to other providers on errors
        """
        self.enable_fallback = enable_fallback
        self.available_providers = []
        
        # Detect all available providers (in priority order)
        # Groq - FIRST PRIORITY - Fast, free, and reliable!
        if os.getenv("GROQ_API_KEY"):
            self.available_providers.append("groq")
        # Gemini - Second priority
        if os.getenv("GEMINI_API_KEY"):
            self.available_providers.append("gemini")
        
        if not self.available_providers:
            raise ValueError("No LLM API key found. Set GROQ_API_KEY or GEMINI_API_KEY in .env file")
        
        # Set primary provider
        if provider is None:
            # Use first available provider
            provider = self.available_providers[0]
        elif provider not in self.available_providers:
            print(f"Warning: {provider} not available, using {self.available_providers[0]}")
            provider = self.available_providers[0]
        
        self.provider = provider
        self.last_error = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == "grok":
            from openai import OpenAI
            api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
            if not api_key:
                raise ValueError("GROK_API_KEY or XAI_API_KEY not found in environment")
            # Grok uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.x.ai/v1"
            )
            self.model = os.getenv("GROK_MODEL", "grok-beta")
        
        elif self.provider == "groq":
            from openai import OpenAI
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment")
            # Groq uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        
        elif self.provider == "openai":
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            self.client = OpenAI(api_key=api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        elif self.provider == "gemini":
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment")
            genai.configure(api_key=api_key)
            self.client = genai
            
            # Get model name from env or auto-detect
            model_name = os.getenv("GEMINI_MODEL")
            if model_name:
                # Use specified model
                self.model = genai.GenerativeModel(model_name)
            else:
                # Auto-detect: find first available model
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            model_name = m.name.replace('models/', '')
                            self.model = genai.GenerativeModel(model_name)
                            break
                    if not hasattr(self, 'model') or self.model is None:
                        raise ValueError("No available Gemini models found")
                except Exception as e:
                    raise ValueError(f"Could not initialize Gemini model: {e}. Try setting GEMINI_MODEL in .env")
        
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            self.client = Anthropic(api_key=api_key)
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        functions: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Call LLM with prompt and automatic fallback on errors
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            functions: Function definitions for tool calling (OpenAI only)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        
        Returns:
            LLM response text
        """
        # Try primary provider first
        providers_to_try = [self.provider]
        
        # Add fallback providers if enabled
        if self.enable_fallback:
            for provider in self.available_providers:
                if provider != self.provider:
                    providers_to_try.append(provider)
        
        last_exception = None
        
        for provider in providers_to_try:
            try:
                print(f"Attempting LLM call with provider: {provider}")
                
                # Reinitialize client for this provider if needed
                if provider != self.provider:
                    old_provider = self.provider
                    self.provider = provider
                    self._initialize_client()
                    print(f"→ Switched from {old_provider} to {provider}")
                
                # Call the appropriate method
                if provider == "grok":
                    result = self._call_openai(prompt, system_prompt, functions, temperature, max_tokens)
                elif provider == "groq":
                    result = self._call_openai(prompt, system_prompt, functions, temperature, max_tokens)
                elif provider == "openai":
                    result = self._call_openai(prompt, system_prompt, functions, temperature, max_tokens)
                elif provider == "gemini":
                    result = self._call_gemini(prompt, system_prompt, temperature, max_tokens)
                elif provider == "anthropic":
                    result = self._call_anthropic(prompt, system_prompt, temperature, max_tokens)
                else:
                    continue
                
                # Success!
                if provider != providers_to_try[0]:
                    print(f"✅ Successfully using {provider} after fallback!")
                
                return result
                
            except Exception as e:
                error_msg = str(e).lower()
                last_exception = e
                
                # Check if it's a rate limit error
                if any(err in error_msg for err in ['rate limit', 'quota', 'too many requests', '429']):
                    print(f"⚠️ Rate limit hit on {provider}: {e}")
                    if self.enable_fallback and provider != providers_to_try[-1]:
                        print(f"→ Falling back to next provider...")
                        time.sleep(0.1)  # Minimal delay before trying next provider
                        continue
                # Check if it's a temporary error
                elif any(err in error_msg for err in ['timeout', 'connection', 'unavailable', '503', '502']):
                    print(f"⚠️ Temporary error on {provider}: {e}")
                    if self.enable_fallback and provider != providers_to_try[-1]:
                        print(f"→ Falling back to next provider...")
                        time.sleep(0.1)  # Minimal delay
                        continue
                # Check if it's an auth/permissions error (403, no credits, etc)
                elif any(err in error_msg for err in ['403', 'forbidden', 'permission', 'credits', 'license']):
                    print(f"⚠️ Auth/credits error on {provider}: {e}")
                    if self.enable_fallback and provider != providers_to_try[-1]:
                        print(f"→ Falling back to next provider...")
                        time.sleep(0.1)  # Minimal delay
                        continue
                    else:
                        # Last provider, raise the error
                        raise e
                else:
                    # Other errors, don't fallback
                    raise e
        
        # If all providers failed, raise the last exception
        if last_exception:
            raise last_exception
        else:
            raise ValueError("No LLM providers available")
    
    def _call_openai(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        functions: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Call OpenAI API"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timeout": 30,  # 30 second timeout instead of default
        }
        
        if functions:
            kwargs["functions"] = functions
            kwargs["function_call"] = "auto"
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    def _call_gemini(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Call Gemini API"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            # If model doesn't exist, try to list available models
            if "not found" in str(e).lower() or "404" in str(e):
                try:
                    # Try to get available models
                    models = self.client.list_models()
                    available = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
                    raise ValueError(
                        f"Model not found. Available models: {available}. "
                        f"Set GEMINI_MODEL in .env to one of these."
                    )
                except:
                    raise ValueError(
                        f"Model error: {e}. Try setting GEMINI_MODEL=gemini-1.5-flash in .env"
                    )
            raise
    
    def _call_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Call Anthropic Claude API"""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
            "timeout": 30,  # 30 second timeout
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text
    
    def call_with_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict:
        """
        Call LLM and parse JSON response with automatic fallback
        
        Args:
            prompt: User prompt (should request JSON)
            system_prompt: System prompt
            temperature: Lower temperature for more consistent JSON
        
        Returns:
            Parsed JSON as dictionary
        """
        import json
        
        # Get response using the fallback-enabled call method
        response_text = self.call(prompt, system_prompt, temperature=temperature, max_tokens=2000)
        
        # Try to parse JSON from response
        try:
            # Look for JSON in code blocks or plain text
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()
            
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If parsing fails, return raw text wrapped in dict
            return {"raw_response": response_text, "error": "Failed to parse JSON"}


# Convenience function to get LLM client
def get_llm_client() -> LLMClient:
    """Get initialized LLM client from environment"""
    return LLMClient()
