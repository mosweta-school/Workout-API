from flask import Flask, jsonify
from flask_migrate import Migrate
from .models import db, Workout
from .schemas import workouts_schema

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

if __name__ == "__main__":
    app.run(
        port = 5555,
        debug=True
    )