
import os
import requests
from flask import Flask, request, jsonify, render_template, url_for, session, redirect, render_template_string
from flask_cors import CORS
import uuid
from datetime import datetime
from authlib.integrations.flask_client import OAuth
import random

BADGES = [
    {"name": "Aid Apprentice", "desc": "Completed your first learning module!", "icon": "🔰"},
    {"name": "FAFSA Filer", "desc": "Mastered the FAFSA concepts.", "icon": "📄"},
    {"name": "Aid Analyst", "desc": "Used the Net Price Calculator.", "icon": "🧮"},
    {"name": "Resource Explorer", "desc": "Visited the Resource Hub.", "icon": "🧭"},
    {"name": "Scholarship Seeker", "desc": "Learned about different aid types.", "icon": "💡"},
    {"name": "Knowledge Knight", "desc": "Completed all learning modules!", "icon": "🧠"},
    {"name": "Financial Aid Guru", "desc": "Earned all available badges!", "icon": "👑"},
]

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
AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"
AZURE_OPENAI_API_KEY = "7b7711c1bcd94b4899aaa1d796c4f7ae"
AZURE_OPENAI_API_VERSION = "2023-05-15"

# Function to call Azure OpenAI API
def azure_openai_response(prompt):
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    data = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
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

# --- BEGIN LEARNER MODULE DATA ---
VOCAB = {
    "⭐ Getting Started": [
        {
            "term": "FAFSA (Free Application for Federal Student Aid)",
            "definition": "The official form students must fill out to apply for federal financial aid, including grants, work-study, and loans. It's the single most important application for aid. The FAFSA is also used by many states and colleges to determine eligibility for their own aid programs. It collects detailed information about your family's income, assets, and household size to calculate your Student Aid Index (SAI). The form is updated annually, and recent changes have simplified the process by allowing direct IRS data import. Filing early is crucial as some aid is limited and awarded on a first-come, first-served basis.",
            "example": "The FAFSA opens on October 1st each year. It's crucial to file it as early as possible, as some aid is first-come, first-served. You'll need your Social Security Number, tax returns, and information about your family's finances. For instance, a student from a low-income family might qualify for a full Pell Grant by filing early, while delays could mean missing out on state grants. Even high-income families should file, as it unlocks merit-based aid at many schools. Common mistakes include not reporting all assets or forgetting to sign the form electronically.",
            "quiz": [
                {"q": "What is the main purpose of the FAFSA?", "options": ["To apply for admission to college", "To apply for federal financial aid", "To register for classes", "To get a student ID"], "correct": 1, "explanation": "The FAFSA is used exclusively to determine your eligibility for financial aid from the federal government, and many states and colleges also use it to award their own aid."},
                # ... more quiz questions ...
            ]
        },
        # ... more terms ...
    ],
    "📄 The FAFSA Deep Dive": [
        {
            "term": "Dependency Status",
            "definition": "Determines whether you're considered independent or dependent for FAFSA purposes. Dependent students must provide parental information. Criteria include age (under 24), marital status, children, military service, etc. If you're independent, only your (and spouse's) finances are considered, potentially increasing aid eligibility. Special cases like homelessness or emancipation can grant independent status. Always answer dependency questions carefully as they affect the entire form.",
            "example": "A 22-year-old single student without children is typically dependent and needs parent info. But a 25-year-old is automatically independent. A dependent student whose parents refuse to provide info can still get unsubsidized loans but not other aid. Appeals for dependency overrides are possible but rare and require documentation like court orders.",
            "quiz": [
                {"q": "At what age are you automatically considered independent for FAFSA?", "options": ["18", "24", "21", "26"], "correct": 1, "explanation": "Students 24 and older are independent, using only their own financial info."},
                # ... more quiz questions ...
            ]
        },
        # ... more terms ...
    ],
    # ... other modules ...
}
AID_FACTS = [
    # ... (all the content from learner.py) ...
]
AID_TYPES = [
    # ... (all the content from learner.py) ...
]
CSS = """
    ... (all the CSS from learner.py) ...
"""
NAV = """
    ... (all the NAV HTML from learner.py) ...
"""
# --- END LEARNER MODULE DATA ---

# --- Session Initialization (merge with existing before_request if needed) ---
@app.before_request
def init_session():
    vocab_keys = list(VOCAB.keys())
    if 'current_module' not in session:
        session['current_module'] = vocab_keys[0] if vocab_keys else None
    if 'card_indices' not in session:
        session['card_indices'] = {module: 0 for module in VOCAB}
    if 'module_progress' not in session:
        session['module_progress'] = {module: 0 for module in VOCAB}
    if 'badges' not in session:
        session['badges'] = []
    if 'calculator_uses' not in session:
        session['calculator_uses'] = 0
    if 'resources_visited' not in session:
        session['resources_visited'] = False
    if 'aid_types_visited' not in session:
        session['aid_types_visited'] = False
    if 'active_quiz' not in session:
        session['active_quiz'] = None

# --- Badge Check Helper ---
def check_and_award_badges():
    completed_modules = sum(1 for m in VOCAB if session['module_progress'][m] >= len(VOCAB[m]))
    def add_badge(badge_name):
        if badge_name not in session['badges']:
            session['badges'].append(badge_name)
    if completed_modules > 0:
        add_badge("Aid Apprentice")
    if session['module_progress'].get("📄 The FAFSA Deep Dive", 0) >= len(VOCAB["📄 The FAFSA Deep Dive"]):
        add_badge("FAFSA Filer")
    if session['calculator_uses'] > 0:
        add_badge("Aid Analyst")
    if session['resources_visited']:
        add_badge("Resource Explorer")
    if session['aid_types_visited']:
        add_badge("Scholarship Seeker")
    if completed_modules == len(VOCAB):
        add_badge("Knowledge Knight")
    if len(session['badges']) == len(BADGES) - 1:
        add_badge("Financial Aid Guru")
    session.modified = True

# --- /learning Route ---
@app.route('/learning', methods=['GET', 'POST'])
def learning():
    check_and_award_badges()
    modules = list(VOCAB.keys())
    current_module = request.form.get('module_selector', session.get('current_module', modules[0]))
    session['current_module'] = current_module
    module_vocab = VOCAB[current_module]
    card_index = session['card_indices'].get(current_module, 0)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'previous':
            card_index = max(0, card_index - 1)
        elif action == 'next':
            card_index = min(len(module_vocab) - 1, card_index + 1)
        elif action == 'test':
            session['active_quiz'] = {'module': current_module, 'card_index': card_index, 'level': 1, 'status': 'pending'}
        elif 'option' in request.form:
            level = session['active_quiz']['level']
            quiz = module_vocab[card_index]['quiz'][level - 1]
            selected = int(request.form['option'])
            if selected == quiz['correct']:
                session['active_quiz']['status'] = 'passed'
                if level == 1 and session['module_progress'][current_module] == card_index:
                    session['module_progress'][current_module] += 1
                    check_and_award_badges()
            else:
                session['active_quiz']['status'] = 'failed'
        elif action == 'try_harder' and session['active_quiz']['level'] < 5:
            session['active_quiz']['level'] += 1
            session['active_quiz']['status'] = 'pending'
        elif action == 'try_again':
            session['active_quiz']['status'] = 'pending'
        elif action == 'continue_next':
            session['active_quiz'] = None
            card_index = min(len(module_vocab) - 1, card_index + 1)
        session['card_indices'][current_module] = card_index
        session.modified = True
        return redirect(url_for('learning'))

    module_selector = '<form method="post"><input type="hidden" name="action" value="select_module">'
    for mod in modules:
        checked = 'checked' if mod == current_module else ''
        module_selector += f'<label><input type="radio" name="module_selector" value="{mod}" {checked}> {mod}</label><br>'
    module_selector += '<button type="submit">Switch Module</button></form>'

    content = ''
    if session.get('active_quiz') and session['active_quiz']['card_index'] == card_index:
        quiz_session = session['active_quiz']
        level = quiz_session['level']
        status = quiz_session['status']
        quiz_list = module_vocab[card_index]['quiz']
        if level - 1 < len(quiz_list):
            quiz = quiz_list[level - 1]
            feedback = ''
            buttons = ''
            if status == 'passed':
                feedback = f'<div class="quiz-feedback-correct"><strong>Correct!</strong> {quiz["explanation"]}</div>'
                buttons = '<form method="post">'
                if level < 5 and level < len(quiz_list):
                    buttons += '<button type="submit" name="action" value="try_harder">Try a Harder Question (Level {level + 1})</button>'
                buttons += '<button type="submit" name="action" value="continue_next">Continue to Next Concept →</button></form>'
            elif status == 'failed':
                correct_opt = quiz['options'][quiz['correct']]
                feedback = f'<div class="quiz-feedback-incorrect"><strong>Not quite.</strong> The correct answer was: {correct_opt}.<br>{quiz["explanation"]}</div>'
                buttons = '<form method="post"><button type="submit" name="action" value="try_again">Try This Question Again</button></form>'
            else:
                buttons = '<form method="post">'
                for i, opt in enumerate(quiz['options']):
                    buttons += f'<button type="submit" name="option" value="{i}" class="quiz-option">{opt}</button>'
                buttons += '</form>'
            content = f'<h3>Quiz Level {level}: {quiz["q"]}</h3>{buttons}{feedback}'
        else:
            # Defensive: If quiz level is out of range, reset quiz and show friendly message
            session['active_quiz'] = None
            session.modified = True
            content = '<div class="flashcard"><h3>All quiz levels completed!</h3><p>You have finished all available quiz questions for this concept. Please continue to the next concept or review previous ones.</p></div>'
    else:
        if card_index < len(module_vocab):
            card = module_vocab[card_index]
            content = f"""
            <div class="flashcard">
                <h3>{card['term']}</h3>
                <div class="info-box"><strong>Definition:</strong> {card['definition']}</div>
                <div class="info-box"><strong>Example:</strong> {card['example']}</div>
            </div>
            """
            if card_index == session['module_progress'][current_module]:
                content += '<form method="post"><button type="submit" name="action" value="test">Test My Understanding</button></form>'
            elif card_index < session['module_progress'][current_module]:
                content += '<p>✅ Mastered! You can review or proceed.</p>'
        content += '<form method="post">'
        if card_index > 0:
            content += '<button type="submit" name="action" value="previous">← Previous</button>'
        if card_index < len(module_vocab) - 1:
            content += '<button type="submit" name="action" value="next">Next →</button>'
        content += '</form>'

    module_progress = (session['module_progress'][current_module] / len(module_vocab) * 100) if len(module_vocab) > 0 else 0

    html = f"""
    <style>{CSS}</style>
    <div class="header"><h1>📚 Learning Modules</h1></div>
    {NAV}
    <div class="content">
        {module_selector}
        <h2>{current_module} (Progress: {module_progress:.0f}%)</h2>
        <p>Concept {card_index + 1} of {len(module_vocab)}</p>
        {content}
    </div>
    """
    return render_template_string(html)

# --- /calculator Route ---
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    check_and_award_badges()
    fact = random.choice(AID_FACTS)['fact']
    result = ''
    if request.method == 'POST':
        session['calculator_uses'] += 1
        check_and_award_badges()
        try:
            coa = float(request.form['coa'])
            sai = float(request.form['sai'])
            grants = float(request.form['grants'])
            scholarships = float(request.form['scholarships'])
            gift_aid = grants + scholarships
            net_price = max(0, coa - gift_aid)
            remaining_need = max(0, net_price - sai)
            monthly_payment = 0
            if remaining_need > 0:
                loan_amount = remaining_need
                interest_rate = 0.055
                loan_term_years = 10
                monthly_rate = interest_rate / 12
                num_payments = loan_term_years * 12
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
            result = f"""
            <div class="flashcard">
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
            result = '<p class="quiz-feedback-incorrect">Please enter valid numbers.</p>'

    html = f"""
    <style>{CSS}</style>
    <div class="header"><h1>🧮 Net Price Calculator</h1></div>
    {NAV}
    <div class="content">
        <p>Estimate your out-of-pocket costs.</p>
        <p><strong>Fun Fact:</strong> {fact}</p>
        <form method="post">
            <label>COA: <input type="number" name="coa" required></label>
            <label>SAI: <input type="number" name="sai" required></label>
            <label>Grants: <input type="number" name="grants" required></label>
            <label>Scholarships: <input type="number" name="scholarships" required></label>
            <button type="submit">Calculate</button>
        </form>
        {result}
    </div>
    """
    return render_template_string(html)

# --- /types Route ---
@app.route('/types', methods=['GET'])
def types():
    session['aid_types_visited'] = True
    check_and_award_badges()
    aid_html = ''
    for aid in AID_TYPES:
        color = 'green' if 'No' in aid['repayment'] else 'red'
        aid_html += f"""
        <div class="flashcard">
            <h3>{aid['name']}</h3>
            <p>Type: {aid['type']}</p>
            <p>Repayment: <span style="color:{color};">{aid['repayment']}</span></p>
            <div class="info-box">{aid['description']}</div>
        </div>
        """

    html = f"""
    <style>{CSS}</style>
    <div class="header"><h1>💡 Types of Aid</h1></div>
    {NAV}
    <div class="content">
        <p>Explore the main types of financial aid.</p>
        {aid_html}
    </div>
    """
    return render_template_string(html)

# --- /resources Route ---
@app.route('/resources', methods=['GET'])
def resources():
    session['resources_visited'] = True
    check_and_award_badges()
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
        # Add all categories from original – this is full.
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
            resources_html += f'<div class="info-box"><a href="{item["url"]}" target="_blank">{item["name"]}</a>: {item["desc"]}</div>'

    html = f"""
    <style>{CSS}</style>
    <div class="header"><h1>🧭 Resource Hub</h1></div>
    {NAV}
    <div class="content">
        <p>Trusted links for further help.</p>
        {resources_html}
    </div>
    """
    return render_template_string(html)
# --- END LEARNER MODULE ---

@app.route('/learner')
def learner():
    return redirect(url_for('learning'))

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