
import os
import requests
from flask import Flask, request, jsonify, render_template, url_for, session, redirect, render_template_string
from flask_cors import CORS
import uuid
from datetime import datetime
from authlib.integrations.flask_client import OAuth
import random
from openai_service import openai_client, AZURE_OPENAI_DEPLOYMENT

# Create the Flask app
app = Flask(__name__)
# Session config
app.secret_key = os.urandom(24)
app.config.from_mapping(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# OAuth 2 client setup
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Enable CORS
CORS(app)

# System prompt that the chatbot will use
SYSTEM_PROMPT = (
    "You are AccessEdu, an empathetic AI assistant built to help first-generation and immigrant families understand and plan for college expenses in the United States. "
    "Your core purpose is to make college financial planning simple, clear, and inclusive, especially for those who may face language barriers or lack prior knowledge of the process. "
    "You can: explain the FAFSA process step-by-step in simple language; suggest scholarships based on user details; help families build and adjust a college budget using their income, tuition, and scholarship info; and translate financial aid concepts into everyday terms. "
    "If asked, you can also suggest ways to find educational videos in multiple languages and point to common FAQs. "
    "Always use plain, friendly, and supportive language, as if you’re guiding someone who feels overwhelmed. "
    "If a question is unrelated to college financial planning, politely explain that you can only help with FAFSA, scholarships, budgeting, and related financial topics. "
    "Your mission is to empower every family to feel confident navigating college costs, no matter their background or language."
)

# Your Azure OpenAI details
AZURE_OPENAI_ENDPOINT = "https://bsmp2023.openai.azure.com/"
AZURE_OPENAI_API_KEY = "7b7711c1bcd94b4899aaa1d796c4f7ae"
AZURE_OPENAI_API_VERSION = "2023-05-15"

# Function to call Azure OpenAI API
def azure_openai_response(prompt):
    if not openai_client:
        return "[Error: Azure OpenAI client not initialized]"
    try:
        response = openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
            max_tokens=512,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error calling Azure OpenAI API: {e}]"

TRANSLATION_API_KEY = os.getenv("TRANSLATION_API_KEY") or "50xBq9y2s08yVpghkmopLEevF6FNsXksvmKOuayRxyhpUfbnAZyJJQQJ99BAACHYHv6XJ3w3AAAAACOG0O6p"
TRANSLATION_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
TRANSLATION_REGION = "eastus2"

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '')
    to_lang = data.get('to_lang', 'es')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    path = '/translate'
    constructed_url = TRANSLATION_ENDPOINT + path
    params = {
        'api-version': '3.0',
        'to': [to_lang]
    }
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATION_API_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATION_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{ 'text': text }]
    try:
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        translated = result[0]['translations'][0]['text']
        return jsonify({'translated': translated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test route to check server is running
@app.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', user=user)

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def google_authorize():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

# --- Data Structures for Learner Module ---
# Remove all BADGES, VOCAB, AID_FACTS, AID_TYPES, CUSTOM_CSS, and all learner-related helpers and routes.
# --- END LEARNER MODULE DATA ---

# --- Session Initialization (merge with existing before_request if needed) ---
@app.before_request
def init_session():
    # Remove all learner-related session initialization
    pass

# --- Badge Check Helper ---
# Remove all badge check helper functions

# --- /learning Route ---
# Remove all /learning route logic

# --- /calculator Route ---
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = ''
    if request.method == 'POST':
        try:
            coa = float(request.form['coa'])
            sai = float(request.form['sai'])
            grants = float(request.form['grants'])
            scholarships = float(request.form['scholarships'])
            gift_aid = grants + scholarships
            net_price = coa - gift_aid
            remaining_need = net_price - sai
            monthly_payment = 0
            if remaining_need > 0:
                # Example loan calculation (10 years at 5.5%)
                r = 0.055 / 12
                n = 10 * 12
                monthly_payment = (remaining_need * r * (1 + r) ** n) / ((1 + r) ** n - 1)
            result = f"""
            <div>
                <h3>Results</h3>
                <p>COA: ${coa:,.0f}</p>
                <p>Gift Aid: ${gift_aid:,.0f}</p>
                <p>Net Price: ${net_price:,.0f}</p>
                <p>SAI: ${sai:,.0f}</p>
                <p>Remaining Need: ${remaining_need:,.0f}</p>
            """
            if remaining_need > 0:
                result += f"<p>Estimated Monthly Loan Payment (10 yrs @ 5.5%): ${monthly_payment:,.2f}</p>"
            result += "</div>"
        except ValueError:
            result = '<p style="color:red;">Please enter valid numbers.</p>'

    html = f"""
    <div style='padding: 2rem;'>
        <h1>🧮 Net Price Calculator</h1>
        <div>
        <p>Estimate your out-of-pocket costs.</p>
        <form method="post">
            <label>COA: <input type="number" name="coa" required></label>
            <label>SAI: <input type="number" name="sai" required></label>
            <label>Grants: <input type="number" name="grants" required></label>
            <label>Scholarships: <input type="number" name="scholarships" required></label>
            <button type="submit">Calculate</button>
        </form>
        {result}
        </div>
    </div>
    """
    return render_template_string(html)

# --- /types Route ---
@app.route('/types', methods=['GET'])
def types():
    aid_html = '<div><h1>💡 Types of Aid</h1><ul>'
    aid_html += '<li>Grants: Free money, usually need-based, does not need to be repaid.</li>'
    aid_html += '<li>Scholarships: Free money, usually merit-based, does not need to be repaid.</li>'
    aid_html += '<li>Federal Work-Study: Earned money from a part-time job.</li>'
    aid_html += '<li>Federal Loans: Borrowed money you must repay with interest.</li>'
    aid_html += '</ul></div>'
    return render_template_string(aid_html)

# --- /resources Route ---
@app.route('/resources', methods=['GET'])
def resources():
    resources_html = ''
    categories = {
        "Official Sites": [
            {"name": "StudentAid.gov", "url": "https://studentaid.gov", "desc": "File FAFSA, manage loans."},
            {"name": "CSS Profile", "url": "https://cssprofile.collegeboard.org", "desc": "For institutional aid."}
        ],
        "Scholarship Searches": [
            {"name": "Fastweb", "url": "https://www.fastweb.com", "desc": "Free matching service."},
            {"name": "Scholarships.com", "url": "https://www.scholarships.com", "desc": "Thousands of opportunities."}
        ],
        "Loan Info": [
            {"name": "Loan Forgiveness", "url": "https://studentaid.gov/manage-loans/forgiveness-cancellation", "desc": "PSLF and more."}
        ],
        "Scam Avoidance": [
            {"name": "FSA Scam Warnings", "url": "https://studentaid.gov/understand-aid/eligibility/requirements/avoid-scams", "desc": "Spot and report scams."}
        ]
    }
    for cat, items in categories.items():
        resources_html += f'<h3>{cat}</h3>'
        for item in items:
            resources_html += f'<div style="background:#f0f0f0;padding:10px;margin-bottom:8px;border-radius:6px;"><a href="{item["url"]}" target="_blank">{item["name"]}</a>: {item["desc"]}</div>'
    html = f"""
    <div style='padding: 2rem;'>
        <h1>🧭 Resource Hub</h1>
        <div>
        <p>Trusted links for further help.</p>
        {resources_html}
        </div>
    </div>
    """
    return render_template_string(html)
# --- END LEARNER MODULE ---

# Remove the /learner route entirely.

@app.route('/chatbot')
def chatbot():
    return render_template('index.html')

@app.route('/budget-scanner')
def budget_scanner():
    return render_template('budget_scanner.html')

@app.route('/scholarship-finder')
def scholarship_finder():
    return render_template('scholarship_finder.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

# Chatbot route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    answer = azure_openai_response(user_input)
    return jsonify({'response': answer})

@app.route('/find-scholarships', methods=['POST'])
def find_scholarships():
    data = request.get_json()
    major = data.get('major', '')
    gpa = data.get('gpa', '')
    location = data.get('location', '')
    grade_level = data.get('grade_level', '')
    essay = data.get('essay', '')
    today = datetime.now().strftime('%Y-%m-%d')
    # Compose a prompt for the AI
    prompt = (
        f"List 5 scholarships (each as a Markdown-style bullet point) that a student could apply for given these details: "
        f"Major: {major}, GPA: {gpa}, Location: {location}, Grade Level: {grade_level}, "
        f"Essay Requirement: {essay}. "
        f"For each, include: (1) the scholarship name as a clickable hyperlink to the application page, (2) a short description, and (3) the application deadline (must be after {today}). "
        f"Use real or plausible links and deadlines. Only show scholarships with deadlines after {today}. "
        f"Format as a Markdown-style list."
    )
    answer = azure_openai_response(prompt)
    return jsonify({'results': answer})

if __name__ == "__main__":
    app.run(debug=True, port=8000)