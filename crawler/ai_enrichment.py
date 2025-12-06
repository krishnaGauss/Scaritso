import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def analyze_content(text, model_name="gemini-2.5-pro"):
    """
    Analyzes the provided text using Gemini to generate a summary, tags, and a quality score.
    
    Args:
        text (str): The content to analyze.
        model_name (str): The model version to use.
        
    Returns:
        dict: A dictionary containing 'summary', 'tags', and 'score'.
              Returns None if analysis fails or API is not configured.
    """
    if not configure_gemini():
        print("Warning: GEMINI_API_KEY not found. Skipping AI enrichment.")
        return None

    try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        You are an expert content curator. Analyze the following text and return a JSON object with these 3 fields:
        1. "summary": A concise 2-sentence summary of the content.
        2. "tags": A list of 5 relevant keyword tags.
        3. "score": An integer from 1 to 10 rating the information density and quality.

        Output ONLY valid JSON. Do not include markdown formatting like ```json.
        
        Text to analyze:
        {text[:10000]}  # Truncate to avoid context limit issues if text is huge
        """
        
        response = model.generate_content(prompt)
        
        # Clean up response text if necessary (sometimes models add backticks)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        return json.loads(response_text)
        
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return None
