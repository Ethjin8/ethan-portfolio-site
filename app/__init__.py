import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Ethan Jin", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Me")

@app.route('/experience')
def experience():
    jobs = [
        {
            "role": "Production Engineering Fellow",
            "company": "MLH Fellowship",
            "dates": "Jun 2026 – Present",
            "description": "Building and deploying a portfolio site using Flask. Learning about CI/CD, Linux, and site reliability engineering.",
        },
        {
            "role": "Undergraduate Researcher",
            "company": "Materials Design Through Dynamics Lab @ UCLA",
            "dates": "Nov 2025 – Present",
            "description": "Building a full-stack AI platform for substance analysis. Designed a FastAPI backend selecting from 18,000 pre-trained neural networks with a custom LRU cache.",
        },
        {
            "role": "Software Engineer",
            "company": "Association for Computing Machinery @ UCLA",
            "dates": "Oct 2025 – Present",
            "description": "Maintaining the org website for 3,500+ members. Migrated internship apps to MongoDB and created REST API endpoints with auth and rate limiting.",
        },
        {
            "role": "Software Engineering Intern",
            "company": "San Diego Supercomputer Center",
            "dates": "Jun 2023 – Aug 2024",
            "description": "Built Python scripts to process 150+ system dependency files on the Expanse supercomputer. Created a CLI tool analyzing 13M+ lines of module logs.",
        },
    ]
    education = [
        {
            "school": "University of California, Los Angeles (UCLA)",
            "degree": "B.S. Computer Engineering",
            "dates": "Sep 2025 – Jun 2028",
        },
    ]
    return render_template('experience.html', title="Experience", jobs=jobs, education=education)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies")

@app.route('/map')
def map_page():
    return render_template('map.html', title="Map")
