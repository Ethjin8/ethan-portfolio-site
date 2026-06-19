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
            "name": "Basketball",
            "image": "./static/img/basketball.jpeg",
            "description": "Huge Warriors fan. Love playing pickup games and watching the NBA.",
        },
        {
            "name": "Badminton",
            "image": "./static/img/badminton.jpeg",
            "description": "One of my favorite sports to play — fast-paced and always a good time.",
        },
        {
            "name": "Gym",
            "image": "./static/img/gym.jpeg",
            "description": "Staying active and pushing my limits in the weight room.",
        },
        {
            "name": "Movies & TV Shows",
            "image": "./static/img/movies.png",
            "description": "Always looking for a great show to binge. Currently into Daredevil.",
        },
        {
            "name": "Reading",
            "image": "./static/img/reading.png",
            "description": "Big fan of fantasy — Brandon Sanderson's Stormlight Archive is a favorite.",
        },
    ]
    return render_template('hobbies.html', title="Hobbies", hobbies=hobbies_list)

@app.route('/map')
def map_page():
    return render_template('map.html', title="Map")
