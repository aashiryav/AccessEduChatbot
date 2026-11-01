AccessEduChatbot

A comprehensive educational resource web application that helps students navigate college financial planning, scholarship opportunities, and financial literacy. AccessEDU was built in summer 2025 as part of the Blacks at Microsoft Summer Mentorship Program, which provided the Azure resources used by the app. I wrote the code and designed the layouts in Figma, as team leader of a five-person team.

![AccessEDU Logo](static/images/a3e929fd-63d2-4f73-abba-98a2528d3efb-removebg-preview.png)

Development History
AccessEDU was developed locally during the Blacks at Microsoft Summer Mentorship Program in summer 2025 and uploaded to GitHub after the program's final hackathon presentation. Because of this, the commit history doesn't show the original thorough development process. 

Features
- FAFSA Chatbot: Get answers to your questions about FAFSA and financial aid
- Scholarship Finder: Find personalized scholarship opportunities based on your profile
- Budget Scanner: Plan and analyze your college finances with a detailed budget tool
- Learning Center: Access educational resources to improve financial literacy

Prerequisites
- Python 3.6 or higher
- OpenAI API key (for chatbot functionality)
- Modern web browser

Installation

For Windows Users

1. Clone the repository:

   ```bash
   git clone https://github.com/aashiryav/AccessEduChatbot.git
   cd AccessEduChatbot
   ```

2. Run the setup script:

   ```bash
   setup.bat
   ```

3. Set your OpenAI API key:

   ```bash
   set OPENAI_API_KEY=your_api_key_here
   ```

4. Run the application:

   ```bash
   python app.py
   ```

For macOS/Linux Users

1. Clone the repository:

   ```bash
   git clone https://github.com/aashiryav/AccessEduChatbot.git
   cd AccessEduChatbot
   ```

2. Make the setup script executable:

   ```bash
   chmod +x setup.sh
   ```

3. Run the setup script:

   ```bash
   ./setup.sh
   ```

4. Set your OpenAI API key:

   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

5. Run the application:

   ```bash
   python app.py
   ```

Project Structure

- `app.py`: Main Flask application
- `openai_service.py`: OpenAI integration for chatbot functionality
- `scholarships.json`: Database of scholarship opportunities
- `static/`: Static assets (CSS, images)
- `templates/`: HTML templates
  - `base.html`: Base template with site header and navigation
  - `home.html`: Landing page
  - `budget_scanner.html`: Budget planning tool
  - `scholarship_finder.html`: Scholarship discovery interface
  - `learner.html`: Learning center

Using the Application

1. Home Page: Navigate to `http://127.0.0.1:5000/` after starting the application
2. FAFSA Help: Ask questions about financial aid and get AI-powered responses
3. Scholarship Finder: Enter your academic profile to find matching scholarships
4. Budget Scanner: Plan your college finances with detailed analysis tools
5. Learner: Access educational resources on financial literacy

Development

Adding New Features

1. Create new route handlers in `app.py`
2. Add template files in the `templates/` directory
3. Update the navigation in `base.html` or individual templates

Styling

- All styles are inline within HTML templates
- The color scheme uses a blue theme (#23406e, #002F5B) throughout

Adding New Scholarships

Add new scholarship entries to the `scholarships.json` file in the following format:

```json
{
  "name": "Scholarship Name",
  "amount": "$1000",
  "deadline": "December 31, 2025",
  "requirements": "3.5 GPA, High School Senior",
  "link": "https://example.com/scholarship"
}
```

Troubleshooting

- OpenAI API errors: Make sure your API key is set correctly in environment variables
- Missing dependencies: Run `pip install -r requirements.txt` to ensure all packages are installed
- Page not found errors: Check that routes in `app.py` match your URL paths
