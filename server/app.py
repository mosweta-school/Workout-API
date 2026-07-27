from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .models import db, Workout, Exercise
from .schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
)

app = Flask(__name__)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "instance" / "app.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db) 

import os

with app.app_context():
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Database file:", db.engine.url.database)
    print("Absolute path:", os.path.abspath(db.engine.url.database))
@app.route("/")
def home():
    return {
        "message": "workout tracker API is running"
    }
@app.route("/workouts", methods=["GET"])
def get_workouts():
    """
    Return all workouts.
    """

    workouts = Workout.query.all()

    result = workouts_schema.dump(workouts)

    return jsonify(result), 200

@app.get("/workouts/<int:id>")
def get_workout(id):
    """
    Return a single workout by its ID.
    """

    workout = Workout.query.get(id)

    if workout is None:
        return jsonify({
            "error": "Workout not found."
        }), 404

    return jsonify(workout_schema.dump(workout)), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    """
    Create a new workout.
    """

    data = request.get_json()

    try:
        validated_data = workout_schema.load(data)

        workout = Workout(**validated_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    """
    Delete a workout by its ID.
    """

    workout = db.session.get(Workout, id)

    if workout is None:
        return jsonify({
            "error": "Workout not found."
        }), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully."
    }), 200

@app.route("/exercises", methods=["GET"])
def get_exercises():
    """
    Return all exercises.
    """

    exercises = Exercise.query.all()

    return jsonify(
        exercises_schema.dump(exercises)
    ), 200
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    """
    Return a single exercise by its ID.
    """

    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return jsonify({
            "error": "Exercise not found."
        }), 404

    return jsonify(
        exercise_schema.dump(exercise)
    ), 200
if __name__ == "__main__":
    app.run(
        port = 5555,
        debug=True
    )