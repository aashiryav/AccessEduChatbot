from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import plotly.graph_objs as go
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

BADGES = [
    {"name": "Aid Apprentice", "desc": "Completed your first learning module!", "icon": "🔰"},
    {"name": "FAFSA Filer", "desc": "Mastered the FAFSA concepts.", "icon": "📄"},
    {"name": "Aid Analyst", "desc": "Used the Net Price Calculator.", "icon": "🧮"},
    {"name": "Resource Explorer", "desc": "Visited the Resource Hub.", "icon": "🧭"},
    {"name": "Scholarship Seeker", "desc": "Learned about different aid types.", "icon": "💡"},
    {"name": "Knowledge Knight", "desc": "Completed all learning modules!", "icon": "🧠"},
    {"name": "Financial Aid Guru", "desc": "Earned all available badges!", "icon": "👑"},
]

@app.route('/')
def learner_home():
    # Example: show all badges
    return render_template('learner.html', badges=BADGES)

if __name__ == '__main__':
    app.run(debug=True)
