from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from config import Config
from models.user import db, User, FitnessAssessment, FitnessActivity


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------- DATABASE ----------------

    db.init_app(app)

    # ---------------- LOGIN ----------------

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ---------------- CREATE DATABASE TABLES ----------------

    with app.app_context():
        db.create_all()

    # ---------------- HOME ----------------

    @app.route("/")
    def index():
        return render_template("index.html")

    # ---------------- DASHBOARD ----------------

    @app.route("/dashboard")
    @login_required
    def dashboard():

        assessments = FitnessAssessment.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessAssessment.created_at.desc()
        ).all()

        activities = FitnessActivity.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessActivity.date.desc(),
            FitnessActivity.created_at.desc()
        ).all()

        latest = assessments[0] if assessments else None

        # ---------------- BMI ----------------

        bmi_category = None

        if latest:

            if latest.bmi < 18.5:
                bmi_category = "Underweight"

            elif latest.bmi < 25:
                bmi_category = "Healthy"

            elif latest.bmi < 30:
                bmi_category = "Overweight"

            else:
                bmi_category = "Obesity"

        # ---------------- WATER ----------------

        water = None

        if latest:
            water = round(latest.weight * 0.035, 1)

        # ---------------- DAILY ACTIVITY ----------------

        today = datetime.utcnow().date()

        today_activities = FitnessActivity.query.filter_by(
            user_id=current_user.id,
            date=today
        ).all()

        today_steps = sum(
            activity.steps for activity in today_activities
        )

        today_duration = sum(
            activity.duration for activity in today_activities
        )

        today_calories = sum(
            activity.calories_burned
            for activity in today_activities
        )

        # ---------------- WEEKLY ACTIVITY ----------------

        week_start = today - timedelta(days=6)

        weekly_activities = FitnessActivity.query.filter(
            FitnessActivity.user_id == current_user.id,
            FitnessActivity.date >= week_start,
            FitnessActivity.date <= today
        ).all()

        weekly_steps = sum(
            activity.steps for activity in weekly_activities
        )

        weekly_duration = sum(
            activity.duration for activity in weekly_activities
        )

        weekly_calories = sum(
            activity.calories_burned
            for activity in weekly_activities
        )

        # ---------------- PROGRESS BAR VALUES ----------------

        step_progress = min(
            round((today_steps / 10000) * 100),
            100
        )

        workout_progress = min(
            round((today_duration / 30) * 100),
            100
        )

        calorie_progress = min(
            round((today_calories / 500) * 100),
            100
        )

        return render_template(
            "dashboard.html",
            latest=latest,
            assessments=assessments,
            activities=activities,
            bmi_category=bmi_category,
            water=water,
            today=today,
            today_steps=today_steps,
            today_duration=today_duration,
            today_calories=today_calories,
            weekly_steps=weekly_steps,
            weekly_duration=weekly_duration,
            weekly_calories=weekly_calories,
            step_progress=step_progress,
            workout_progress=workout_progress,
            calorie_progress=calorie_progress
        )

    # ---------------- FITNESS PLAN ----------------

    @app.route("/plan", methods=["GET", "POST"])
    @login_required
    def plan():

        if request.method == "POST":

            try:
                age = int(request.form["age"])
                height = float(request.form["height"])
                weight = float(request.form["weight"])
                activity = request.form["activity"]

            except (ValueError, KeyError):

                flash("Please enter valid information.")

                return redirect(url_for("plan"))

            if age < 13 or age > 120:

                flash("Please enter a valid age.")

                return redirect(url_for("plan"))

            if height < 100 or height > 250:

                flash("Please enter a valid height.")

                return redirect(url_for("plan"))

            if weight < 20 or weight > 300:

                flash("Please enter a valid weight.")

                return redirect(url_for("plan"))

            if activity not in ["low", "moderate", "high"]:

                flash("Please select a valid activity level.")

                return redirect(url_for("plan"))

            height_m = height / 100

            bmi = weight / (height_m ** 2)

            bmr = (
                (10 * weight)
                + (6.25 * height)
                - (5 * age)
                + 5
            )

            if activity == "low":
                calories = bmr * 1.2

            elif activity == "moderate":
                calories = bmr * 1.55

            else:
                calories = bmr * 1.725

            bmi = round(bmi, 1)
            calories = round(calories)

            assessment = FitnessAssessment(
                user_id=current_user.id,
                age=age,
                height=height,
                weight=weight,
                activity=activity,
                bmi=bmi,
                calories=calories
            )

            db.session.add(assessment)
            db.session.commit()

            return render_template(
                "result.html",
                bmi=bmi,
                calories=calories,
                age=age,
                height=height,
                weight=weight,
                activity=activity,
                assessment=assessment
            )

        return render_template("plan.html")

    # ---------------- SIGN UP ----------------

    @app.route("/signup", methods=["GET", "POST"])
    def signup():

        if request.method == "POST":

            name = request.form["name"].strip()
            email = request.form["email"].strip().lower()
            password = request.form["password"]

            if not name:

                flash("Please enter your name.")

                return redirect(url_for("signup"))

            if not email:

                flash("Please enter your email.")

                return redirect(url_for("signup"))

            if len(password) < 8:

                flash(
                    "Password must be at least 8 characters long."
                )

                return redirect(url_for("signup"))

            existing_user = User.query.filter_by(
                email=email
            ).first()

            if existing_user:

                flash(
                    "Email already registered. Please log in."
                )

                return redirect(url_for("login"))

            hashed_password = generate_password_hash(password)

            user = User(
                name=name,
                email=email,
                password=hashed_password
            )

            db.session.add(user)
            db.session.commit()

            flash(
                "Account created successfully. Please log in."
            )

            return redirect(url_for("login"))

        return render_template("signup.html")

    # ---------------- LOGIN ----------------

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form["email"].strip().lower()
            password = request.form["password"]

            user = User.query.filter_by(
                email=email
            ).first()

            if user and check_password_hash(
                user.password,
                password
            ):

                login_user(user)

                return redirect(
                    url_for("dashboard")
                )

            flash("Invalid email or password.")

        return render_template("login.html")

    # ---------------- FITNESS ACTIVITY ----------------

    @app.route("/fitness-activity", methods=["GET", "POST"])
    @login_required
    def fitness_activity():

        if request.method == "POST":

            try:
                activity_date = request.form["date"]
                steps = int(request.form["steps"])
                workout_type = request.form["workout_type"].strip()
                duration = int(request.form["duration"])
                calories_burned = int(
                    request.form["calories_burned"]
                )

            except (ValueError, KeyError):

                flash("Please enter valid fitness information.")

                return redirect(
                    url_for("fitness_activity")
                )

            if steps < 0:

                flash("Steps cannot be negative.")

                return redirect(
                    url_for("fitness_activity")
                )

            if duration < 0:

                flash("Workout duration cannot be negative.")

                return redirect(
                    url_for("fitness_activity")
                )

            if calories_burned < 0:

                flash("Calories burned cannot be negative.")

                return redirect(
                    url_for("fitness_activity")
                )

            if not workout_type:

                flash("Please enter a workout type.")

                return redirect(
                    url_for("fitness_activity")
                )

            try:

                selected_date = datetime.strptime(
                    activity_date,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                flash("Please enter a valid date.")

                return redirect(
                    url_for("fitness_activity")
                )

            activity = FitnessActivity(
                user_id=current_user.id,
                date=selected_date,
                steps=steps,
                workout_type=workout_type,
                duration=duration,
                calories_burned=calories_burned
            )

            db.session.add(activity)
            db.session.commit()

            flash(
                "Fitness activity saved successfully!"
            )

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "fitness_activity.html"
        )

    # ---------------- WORKOUT ----------------

    @app.route("/workout")
    @login_required
    def workout():

        goal = request.args.get(
            "goal",
            "general"
        )

        workouts = [

            {
                "day": "MONDAY",
                "name": "Full Body",
                "exercises": [
                    "Bodyweight Squats — 3 × 12",
                    "Push-ups — 3 × 8",
                    "Glute Bridges — 3 × 12",
                    "Plank — 3 × 30 seconds"
                ]
            },

            {
                "day": "TUESDAY",
                "name": "Cardio",
                "exercises": [
                    "Brisk Walk — 20 minutes",
                    "Jumping Jacks — 3 × 30 seconds",
                    "High Knees — 3 × 30 seconds"
                ]
            },

            {
                "day": "WEDNESDAY",
                "name": "Recovery",
                "exercises": [
                    "Easy Walk — 20 minutes",
                    "Stretching — 10 minutes",
                    "Deep Breathing — 5 minutes"
                ]
            },

            {
                "day": "THURSDAY",
                "name": "Upper Body",
                "exercises": [
                    "Push-ups — 3 × 8",
                    "Wall Push-ups — 3 × 12",
                    "Plank Shoulder Taps — 3 × 10",
                    "Superman — 3 × 12"
                ]
            },

            {
                "day": "FRIDAY",
                "name": "Lower Body",
                "exercises": [
                    "Bodyweight Squats — 3 × 12",
                    "Reverse Lunges — 3 × 10",
                    "Glute Bridges — 3 × 15",
                    "Calf Raises — 3 × 15"
                ]
            },

            {
                "day": "SATURDAY",
                "name": "Light Activity",
                "exercises": [
                    "Walking — 30 minutes",
                    "Light Stretching — 10 minutes"
                ]
            },

            {
                "day": "SUNDAY",
                "name": "Rest Day",
                "exercises": [
                    "Rest",
                    "Relax",
                    "Prepare for the week ahead"
                ]
            }

        ]

        return render_template(
            "workout.html",
            goal=goal,
            workouts=workouts
        )

    # ---------------- NUTRITION ----------------

    @app.route("/nutrition")
    @login_required
    def nutrition():

        assessments = FitnessAssessment.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessAssessment.created_at.desc()
        ).all()

        latest = assessments[0] if assessments else None

        return render_template(
            "nutrition.html",
            latest=latest
        )

    # ---------------- WATER TRACKER ----------------

    @app.route("/water")
    @login_required
    def water():

        latest = FitnessAssessment.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessAssessment.created_at.desc()
        ).first()

        water_target = None

        if latest:

            water_target = round(
                latest.weight * 0.035,
                1
            )

        return render_template(
            "water.html",
            water_target=water_target
        )

    # ---------------- PROGRESS ----------------

    @app.route("/progress")
    @login_required
    def progress():

        assessments = FitnessAssessment.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessAssessment.created_at.desc()
        ).all()

        activities = FitnessActivity.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessActivity.date.desc(),
            FitnessActivity.created_at.desc()
        ).all()

        # ---------------- WEEKLY SUMMARY ----------------

        today = datetime.utcnow().date()

        week_start = today - timedelta(days=6)

        weekly_activities = FitnessActivity.query.filter(
            FitnessActivity.user_id == current_user.id,
            FitnessActivity.date >= week_start,
            FitnessActivity.date <= today
        ).all()

        weekly_steps = sum(
            activity.steps for activity in weekly_activities
        )

        weekly_duration = sum(
            activity.duration for activity in weekly_activities
        )

        weekly_calories = sum(
            activity.calories_burned
            for activity in weekly_activities
        )

        # ---------------- DAILY SUMMARY ----------------

        today_activities = FitnessActivity.query.filter_by(
            user_id=current_user.id,
            date=today
        ).all()

        today_steps = sum(
            activity.steps for activity in today_activities
        )

        today_duration = sum(
            activity.duration for activity in today_activities
        )

        today_calories = sum(
            activity.calories_burned
            for activity in today_activities
        )

        # ---------------- PROGRESS VALUES ----------------

        step_progress = min(
            round((today_steps / 10000) * 100),
            100
        )

        workout_progress = min(
            round((today_duration / 30) * 100),
            100
        )

        calorie_progress = min(
            round((today_calories / 500) * 100),
            100
        )

        return render_template(
            "progress.html",
            assessments=assessments,
            activities=activities,
            today=today,
            today_steps=today_steps,
            today_duration=today_duration,
            today_calories=today_calories,
            weekly_steps=weekly_steps,
            weekly_duration=weekly_duration,
            weekly_calories=weekly_calories,
            step_progress=step_progress,
            workout_progress=workout_progress,
            calorie_progress=calorie_progress
        )

    # ---------------- PROFILE ----------------

    @app.route("/profile")
    @login_required
    def profile():

        assessments = FitnessAssessment.query.filter_by(
            user_id=current_user.id
        ).order_by(
            FitnessAssessment.created_at.desc()
        ).all()

        latest = assessments[0] if assessments else None

        return render_template(
            "profile.html",
            assessments=assessments,
            latest=latest
        )

    # ---------------- LOGOUT ----------------

    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        return redirect(
            url_for("index")
        )

    return app


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)