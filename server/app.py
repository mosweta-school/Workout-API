from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .models import db, Workout, Exercise, WorkoutExercise
from .schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
)
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
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

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    """
    Return a single workout by its ID.
    """

    workout = db.session.get(Workout, id)

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
    except ValidationError as err:
        return jsonify({
            "errors": err.messages
        }), 400
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

@app.route("/exercises", methods=["POST"])
def create_exercise():
    """
    Create a new exercise.
    """

    data = request.get_json()

    try:
        validated_data = exercise_schema.load(data)

        exercise = Exercise(**validated_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(
            exercise_schema.dump(exercise)
        ), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "An exercise with that name already exists."
        }), 400

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    """
    Delete an exercise by its ID.
    """

    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return jsonify({
            "error": "Exercise not found."
        }), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully."
    }), 200

@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    """
    Add an exercise to a workout.
    """

    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({
            "error": "Workout not found."
        }), 404

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({
            "error": "Exercise not found."
        }), 404

    data = request.get_json()

    try:
        validated_data = workout_exercise_schema.load(data)

        validated_data["workout_id"] = workout_id
        validated_data["exercise_id"] = exercise_id

        workout_exercise = WorkoutExercise(**validated_data)

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify(
            workout_exercise_schema.dump(workout_exercise)
        ), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "Exercise already exists in this workout."
        }), 400

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 400
if __name__ == "__main__":
    app.run(
        port = 5555,
        debug=True
    )