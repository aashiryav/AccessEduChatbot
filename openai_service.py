import json
import os
import logging
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Azure OpenAI configuration (load from environment if available, else use defaults)
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://bsmp2023.openai.azure.com/')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', '7b7711c1bcd94b4899aaa1d796c4f7ae')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-35-turbo')

# BSMP24 (alternate chat or translation API)
AZURE_OPENAI_ENDPOINT_BSMP24 = os.getenv('AZURE_OPENAI_ENDPOINT_BSMP24', 'https://bsmp24.openai.azure.com/')
AZURE_OPENAI_API_KEY_BSMP24 = os.getenv('AZURE_OPENAI_API_KEY_BSMP24', 'eae439b382754a94a30bb3db8f9ada07')

# Translation API
TRANSLATION_API_KEY = "50xBq9y2s08yVpghkmopLEevF6FNsXksvmKOuayRxyhpUfbnAZyJJQQJ99BAACHYHv6XJ3w3AAAAACOG0O6p"

# Initialize Azure OpenAI client only if credentials are available
openai_client = None
if AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT:
    try:
        openai_client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version="2024-02-01"
        )
        logging.info("Azure OpenAI client initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize Azure OpenAI client: {e}")
        openai_client = None
else:
    logging.warning("Azure OpenAI credentials not found, AI features will be disabled")

def find_scholarships_with_ai(scholarships, grade_level, gpa, gender, major, essay_preference):
    """
    Use Azure OpenAI to intelligently match scholarships based on user criteria
    """
    # If Azure OpenAI client is not available, fall back to basic filtering
    if not openai_client:
        logging.warning("Azure OpenAI client not available, using basic filtering")
        return basic_scholarship_filter(scholarships, grade_level, gpa, gender, major, essay_preference)
    
    try:
        # Create a prompt for the AI to analyze scholarships
        user_profile = f"""
        Student Profile:
        - Grade Level: {grade_level}
        - GPA: {gpa if gpa else 'Not specified'}
        - Gender: {gender}
        - Intended Major: {major if major else 'Not specified'}
        - Essay Preference: {essay_preference}
        """
        
        scholarships_text = json.dumps(scholarships[:20], indent=2)  # Limit to first 20 for token efficiency
        
        prompt = f"""
        You are an expert scholarship advisor. Based on the student profile below, analyze the provided scholarships and select the most relevant matches.

        {user_profile}

        Available Scholarships:
        {scholarships_text}

        Instructions:
        1. Consider eligibility requirements, GPA requirements, major preferences, gender requirements, and essay preferences
        2. Select the top 10 most relevant scholarships
        3. Rank them by relevance (most relevant first)
        4. Only include scholarships the student is likely eligible for
        5. If essay preference is "no", prioritize scholarships without essay requirements
        6. If essay preference is "yes", include scholarships with essay requirements
        7. Match major preferences when possible

        Return your response as a JSON object with this format:
        {{
            "matched_scholarships": [
                {{
                    "id": "scholarship_id",
                    "relevance_score": 0.95,
                    "match_reasons": ["reason1", "reason2"]
                }}
            ]
        }}
        """
        
        response = openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are an expert scholarship matching advisor. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")
        ai_response = json.loads(content)
        matched_ids = [match["id"] for match in ai_response.get("matched_scholarships", [])]
        
        # Filter and sort scholarships based on AI recommendations
        matched_scholarships = []
        scholarship_dict = {s["id"]: s for s in scholarships}
        
        for match in ai_response.get("matched_scholarships", []):
            scholarship_id = match["id"]
            if scholarship_id in scholarship_dict:
                scholarship = scholarship_dict[scholarship_id].copy()
                scholarship["relevance_score"] = match.get("relevance_score", 0.5)
                scholarship["match_reasons"] = match.get("match_reasons", [])
                matched_scholarships.append(scholarship)
        
        logging.debug(f"AI matched {len(matched_scholarships)} scholarships")
        return matched_scholarships
        
    except Exception as e:
        logging.error(f"Error in AI scholarship matching: {str(e)}")
        # Fallback to basic filtering if AI fails
        return basic_scholarship_filter(scholarships, grade_level, gpa, gender, major, essay_preference)

def basic_scholarship_filter(scholarships, grade_level, gpa, gender, major, essay_preference):
    """
    Fallback basic filtering when AI is not available
    """
    filtered = []
    
    for scholarship in scholarships:
        # Basic eligibility checks
        eligible = True
        
        # Check GPA requirement
        if gpa and scholarship.get("min_gpa"):
            try:
                if float(gpa) < float(scholarship["min_gpa"]):
                    eligible = False
            except (ValueError, TypeError):
                pass
        
        # Check gender requirement
        if scholarship.get("gender_requirement") and scholarship["gender_requirement"].lower() != "any":
            if gender.lower() != scholarship["gender_requirement"].lower():
                eligible = False
        
        # Check essay preference
        if essay_preference == "no" and scholarship.get("requires_essay", False):
            eligible = False
        elif essay_preference == "yes" and not scholarship.get("requires_essay", True):
            eligible = False
        
        if eligible:
            scholarship["relevance_score"] = 0.5
            scholarship["match_reasons"] = ["Basic eligibility match"]
            filtered.append(scholarship)
    
    # Sort by amount (descending) as a basic ranking
    filtered.sort(key=lambda x: float(x.get("amount", "0").replace("$", "").replace(",", "")), reverse=True)
    
    return filtered[:10]  # Return top 10
