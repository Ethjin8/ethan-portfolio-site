import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

# If TESTING=true is set in the environment (our test files do this
# before importing `app`), use an in-memory SQLite DB instead of real
# MySQL. This lets tests run without a live database server.
if os.getenv("TESTING") == "true":
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


# ---PAGE ROUTING---
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
            "description": "Always looking for a great show to binge. Currently into Daredevil: Born Again.",
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
    locations = [
        {"name": "San Diego, CA", "lat": 32.7157, "lng": -117.1611},
        {"name": "Los Angeles, CA", "lat": 34.0522, "lng": -118.2437},
        {"name": "San Francisco Bay Area, CA", "lat": 37.7749, "lng": -122.4194},
        {"name": "Zion National Park, UT", "lat": 37.2982, "lng": -113.0263},
        {"name": "Bryce Canyon National Park, UT", "lat": 37.5930, "lng": -112.1871},
        {"name": "Arches National Park, UT", "lat": 38.7331, "lng": -109.5925},
        {"name": "Beijing, China", "lat": 39.9042, "lng": 116.4074},
        {"name": "Wuhan, China", "lat": 30.5928, "lng": 114.3055},
        {"name": "Shanghai, China", "lat": 31.2304, "lng": 121.4737},
        {"name": "Qianjiang, China", "lat": 30.4213, "lng": 112.8994},
        {"name": "Zhangjiajie, China", "lat": 29.1170, "lng": 110.4793},
        {"name": "Sichuan, China", "lat": 30.5728, "lng": 104.0668},
    ]
    return render_template('map.html', title="Map", locations=locations)

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")


# ---DATABASE QUERIES---
@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    # Use .get() instead of [] so a missing key returns None instead of
    # raising a KeyError before we can give a proper error message.
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    # Reject a missing/blank name.
    if not name:
        return "Invalid name", 400

    # Reject missing/blank content.
    if not content:
        return "Invalid content", 400

    # Basic email shape check: needs an "@" and a "." after it.
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

