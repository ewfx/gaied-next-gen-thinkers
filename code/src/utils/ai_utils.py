import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_model(api_key=None, model_name="gemini-2.0-flash"):
    """Initializes the Gemini Pro model with Langchain."""
    if api_key is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)