# Fitness Checker

A full-stack web app that turns a user's height, weight, age, and activity
level into a BMI, a daily calorie target, and personalized fitness
recommendations — with a dashboard that tracks progress over time.

## Features

- **User accounts** — signup/login with hashed passwords (Flask-Login)
- **Fitness assessment** — enter age, height, weight, and activity level to get your BMI and a daily calorie target (Mifflin-St Jeor formula)
- **Daily activity logging** — manually log steps, workout type, duration, and calories burned per day
- **Dashboard** — BMI category, hydration target, and daily/weekly progress bars for steps, workout time, and calories
- **Workout plans** — a 7-day suggested workout schedule
- **Nutrition & water tracking** — recommendations based on your latest assessment
- **Progress history** — view past assessments and daily/weekly activity summaries
- **Profile page** — view your saved assessment history

## Tech stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Auth:** Flask-Login with hashed passwords (Werkzeug)
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates

## Running it locally

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open http://127.0.0.1:5000 in your browser. The SQLite database is created automatically on first run — no manual setup needed.

## Project structure

```
fitness-checker/
├── app.py                     # Flask app factory + all routes
├── config.py                  # App configuration (secret key, database URI)
├── requirements.txt
├── models/
│   └── user.py                 # User, FitnessAssessment, FitnessActivity models
├── static/
│   ├── css/style.css
│   └── js/main.js
├── templates/
│   ├── base.html, index.html, signup.html, login.html,
│   ├── plan.html, result.html, dashboard.html, progress.html,
│   └── workout.html, nutrition.html, water.html, profile.html
└── instance/
    └── fitness.db              # SQLite database (auto-created, not committed)
## Live Demo
https://codealpha-fitnesstracker.onrender.com
