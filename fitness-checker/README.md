# Fitness Checker

A full-stack web app that turns a user's height, weight, age, and activity
level into a BMI, a daily calorie target, and personalized fitness
recommendations — with a dashboard that tracks progress over time.

## Tech stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Auth:** Flask-Login with hashed passwords (Werkzeug)
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates
- **Deployment target:** Render (or similar)

## Project status

- [x] Phase 1 — Project skeleton + landing page
- [ ] Phase 2 — Database models, registration, and login
- [ ] Phase 3 — Fitness assessment form (BMI, calories, activity level)
- [ ] Phase 4 — Recommendations (workouts + nutrition)
- [ ] Phase 5 — Progress dashboard (weight/BMI history + charts)
- [ ] Phase 6 — Deployment

## Running it locally

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Project structure

```
fitness-checker/
├── app.py              # Flask app factory + routes
├── config.py            # App configuration (secret key, database URI)
├── requirements.txt
├── static/
│   ├── css/style.css     # All styling
│   └── js/main.js        # Mobile nav toggle (more JS added later)
├── templates/
│   ├── base.html          # Shared layout: header, nav, footer
│   └── index.html         # Landing page
└── instance/
    └── fitness.db          # SQLite database (created automatically, not committed)
```
