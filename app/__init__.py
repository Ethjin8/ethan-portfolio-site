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
            "description": "Building and deploying portfolio site using Flask. Learning about CI/CD, Linux, and site reliability engineering.",
        },
        {
            "role": "Software Engineering Intern",
            "company": "San Diego Supercomputer Center (SDSC)",
            "dates": "Jun 2025 – Sep 2025",
            "description": "Worked on backend APIs and database optimization. Built internal tools using Python and SQL.",
        },
    ]
    education = [
        {
            "school": "University of California, Los Angeles (UCLA)",
            "degree": "B.S. Computer Science",
            "dates": "Sep 2022 – Jun 2026",
        },
    ]
    return render_template('experience.html', title="Experience", jobs=jobs, education=education)

@app.route('/hobbies')
def hobbies():
    hobbies_list = [
        {
            "name": "Photography",
            "image": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400",
            "description": "I love capturing moments and exploring new perspectives through my camera.",
        },
        {
            "name": "Hiking",
            "image": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=400",
            "description": "Nothing beats a good trail with great views.",
        },
        {
            "name": "Cooking",
            "image": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=400",
            "description": "Experimenting with new recipes and cuisines is my favorite way to unwind.",
        },
        {
            "name": "Gaming",
            "image": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400",
            "description": "From strategy games to casual co-op, I enjoy gaming with friends.",
        },
    ]
    return render_template('hobbies.html', title="Hobbies", hobbies=hobbies_list)

@app.route('/map')
def map_page():
    return render_template('map.html', title="Map")
