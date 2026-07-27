from flask_sqlalchemy import SQLAlchemy

#importing validators
from sqlalchemy.orm import validates

db=SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id= db.Column(
        db.Integer,
        primary_key=True
    )

    name=db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    category=db.Column(
        db.String(50),
        nullable=False
    )

    equipment_needed=db.Column(
        db.Boolean,
        nullable=False
    )
    workout_exercises = db.relationship(
    "WorkoutExercise",
    back_populates="exercise",
    cascade="all, delete-orphan"
)

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):

        if not value:
            raise ValueError("Exercise name is required.")

        value = value.strip()

        if len(value) < 3:
            raise ValueError(
                "Exercise name must be at least 3 characters."
            )

        return value
    @validates("category")
    def validate_category(self, key, value):

        allowed_categories = {
            "Strength",
            "Cardio",
            "Flexibility",
            "Balance"
        }

        value = value.strip().title()

        if value not in allowed_categories:
            raise ValueError(
                f"Category must be one of {allowed_categories}"
            )

        return value
    

class Workout(db.Model):
    __tablename__="workouts"

    id=db.Column(
        db.Integer,
        primary_key=True
    )

    date=db.Column(
        db.Date,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    notes =db.Column(
        db.Text
    )

    workout_exercises = db.relationship(
       "WorkoutExercise",
       back_populates="workout",
       cascade="all, delete-orphan" 
    )
    exercises = db.relationship(
    "Exercise",
    secondary="workout_exercises",
    viewonly=True
)
    @validates("duration_minutes")
    def validate_duration(self, key, value):

        if value <= 0:
            raise ValueError(
                "Workout duration must be greater than zero."
            )

        return value

class WorkoutExercise(db.Model):
    __tablename__="workout_exercises"

    id =db.Column(
        db.Integer,
        primary_key=True
    )

    workout_id=db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id=db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps=db.Column(db.Integer)

    sets =db.Column(db.Integer)

    duration_seconds =db.Column(db.Integer)

    workout =db.relationship(
        "Workout",
        back_populates= "workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )
    @validates("reps", "sets")
    def validate_positive_numbers(self, key, value):

        if value is not None and value <= 0:
            raise ValueError(
                f"{key} must be greater than zero."
            )

        return value
    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):

        if value is not None and value <= 0:
            raise ValueError(
                "Duration seconds must be positive."
            )

        return value
    __table_args__ = (
    db.UniqueConstraint(
        "workout_id",
        "exercise_id",
        name="unique_workout_exercise"
    ),
)
