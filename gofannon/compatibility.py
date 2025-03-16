"""
Compatibility layer for different versions of the OpenAI package.
This allows the code to work with both older and newer versions of the OpenAI API.
"""
import os
import importlib.util
import sys

# Define APIError for compatibility
class APIError(Exception):
    """Exception raised when API request fails."""
    pass

# Check if openai is installed
if importlib.util.find_spec("openai") is not None:
    import openai
    
    # Check if we're using the older version (pre-1.0.0) or newer version
    if not hasattr(openai, 'OpenAI'):
        # We're using the older version, create a compatibility layer
        class OpenAICompat:
            def __init__(self, api_key=None, base_url=None):
                self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
                if base_url:
                    openai.api_base = base_url
                if api_key:
                    openai.api_key = api_key
                
                # Create a chat completions proxy
                self.chat = type('', (), {})()
                self.chat.completions = type('', (), {})()
                self.chat.completions.create = self._create_chat_completion
            
            def _create_chat_completion(self, model, messages, temperature=0.7):
                # Map to the old API
                try:
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=messages,
                        temperature=temperature
                    )
                    return response
                except openai.error.OpenAIError as e:
                    # Convert old API errors to our APIError
                    raise APIError(str(e))
        
        # Replace the OpenAI import with our compatibility class
        sys.modules['openai'].OpenAI = OpenAICompat
        # Also provide APIError
        sys.modules['openai'].APIError = APIError
        print("Using OpenAI compatibility layer for older API version")
    else:
        # For newer versions, just make sure APIError is available
        if not hasattr(openai, 'APIError'):
            sys.modules['openai'].APIError = APIError
        print("Using native OpenAI client (version 1.0.0+)")
else:
    print("OpenAI package not found, functionality will be limited")
