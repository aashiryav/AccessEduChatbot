import os
import json
from openai_service import find_scholarships_with_ai
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
    "Your mission is to empower every family to feel confident navigating college costs, no matter their background or language. "
    "Always keep your replies concise and to the point, unless the user asks for more detail."
)

AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-35-turbo')
AZURE_OPENAI_ENDPOINT_BSMP24 = os.getenv('AZURE_OPENAI_ENDPOINT_BSMP24')
AZURE_OPENAI_API_KEY_BSMP24 = os.getenv('AZURE_OPENAI_API_KEY_BSMP24')
TRANSLATION_API_KEY = os.getenv('TRANSLATION_API_KEY')

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


# --- Import and register Learner Module ---
from learner_module import register_learner_route
register_learner_route(app)

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
# --- END LEARNER MODULE ---

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
    lang = data.get('lang', 'en')
    answer = azure_openai_response(user_input)
    # If language is not English, translate the answer
    if lang and lang != 'en':
        # Use the same translation logic as /translate
        try:
            path = '/translate'
            constructed_url = TRANSLATION_ENDPOINT + path
            params = {
                'api-version': '3.0',
                'to': [lang]
            }
            headers = {
                'Ocp-Apim-Subscription-Key': TRANSLATION_API_KEY,
                'Ocp-Apim-Subscription-Region': TRANSLATION_REGION,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            body = [{ 'text': answer }]
            response = requests.post(constructed_url, params=params, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            translated = result[0]['translations'][0]['text']
            answer = translated
        except Exception as e:
            answer = f"[Error translating: {e}]\n{answer}"
    return jsonify({'response': answer})

import json
from openai_service import find_scholarships_with_ai

def load_scholarships():
    path = os.path.join(os.path.dirname(__file__), 'scholarships.json')
    with open(path) as f:
        data = json.load(f)
    # Works whether the file is a list or {"scholarships": [...]}
    return data.get('scholarships', []) if isinstance(data, dict) else data

@app.route('/find-scholarships', methods=['POST'])
@app.route('/find-scholarships', methods=['POST'])
def find_scholarships():
    data = request.get_json() or {}
    scholarships = load_scholarships()

    def still_open(s):
        try:
            deadline = datetime.strptime(
                s.get('deadline', ''), '%B %d, %Y'
            ).date()
        except (ValueError, TypeError):
            return True
        return deadline >= datetime.now().date()

    available = [s for s in scholarships if still_open(s)]

    matches = find_scholarships_with_ai(
        available,
        grade_level=data.get('grade_level', ''),
        gpa=data.get('gpa', ''),
        gender=data.get('gender', ''),
        major=data.get('major', ''),
        essay_preference=data.get('essay', '')
    )


    if not matches:
        return jsonify({'results': "I couldn't find a match in our scholarship list. "
                                   "Try changing your answers, or ask your school counselor."})

    lines = []
    for s in matches:
        name = s.get('name', 'Scholarship')
        url = s.get('website')
        title = f"[{name}]({url})" if url else name
        line = f"- **{title}**"
        if s.get('amount'):
            line += f" | Amount: {s['amount']}"
        if s.get('deadline'):
            line += f" | Deadline: {s['deadline']}"
        if s.get('description'):
            line += f"\n  {s['description']}"
        reasons = s.get('match_reasons')
        if reasons:
            line += f"\n  Why it fits: {', '.join(reasons)}"
        lines.append(line)

    note = "\n\n*Always confirm details on the scholarship's official page before applying.*"
    return jsonify({'results': "\n".join(lines) + note})

@app.route('/api/mini-advisor', methods=['POST'])
def mini_advisor():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'reply': "Please enter a question for financial advice."}), 400
    # Use a focused system prompt for financial advice
    mini_system_prompt = (
        "You are AdvisorBot, a friendly and practical financial advisor for college-bound families. "
        "Give concise, actionable advice about budgeting, saving, college costs, scholarships, and financial planning. "
        "If the question is not about personal or family finances, politely say you can only help with financial advice."
    )
    try:
        response = openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": mini_system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=256,
            temperature=0.6
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f"Sorry, I couldn't get a response right now. ({e})"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=54321)
