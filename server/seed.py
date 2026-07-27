from .app import app
from .models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    print("🌱 Clearing existing data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()
    print("🏋️ Creating exercises...")

    push_up = Exercise(
        name="Push Up",
        category="Strength",
        equipment_needed=False
    )

    squat = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=False
    )

    bench_press = Exercise(
        name="Bench Press",
        category="Strength",
        equipment_needed=True
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Balance",
        equipment_needed=False
    )
    db.session.add_all([
    push_up,
    squat,
    bench_press,
    running,
    plank
])

    db.session.commit()
    print("💪 Creating workouts...")

    from datetime import date

    morning_strength = Workout(
        date=date(2026, 7, 25),
        duration_minutes=45,
        notes="Upper body strength training."
    )

    leg_day = Workout(
        date=date(2026, 7, 24),
        duration_minutes=60,
        notes="Focused on lower body exercises."
    )

    cardio_session = Workout(
        date=date(2026, 7, 23),
        duration_minutes=30,
        notes="Light cardio and endurance."
    )
    db.session.add_all([
    morning_strength,
    leg_day,
    cardio_session
])

    db.session.commit()
    print("🔗 Linking workouts and exercises...")

    workout_exercises = [

        WorkoutExercise(
            workout=morning_strength,
            exercise=push_up,
            sets=4,
            reps=15
        ),

        WorkoutExercise(
            workout=morning_strength,
            exercise=bench_press,
            sets=4,
            reps=10
        ),

        WorkoutExercise(
            workout=leg_day,
            exercise=squat,
            sets=5,
            reps=12
        ),

        WorkoutExercise(
            workout=leg_day,
            exercise=plank,
            duration_seconds=90
        ),

        WorkoutExercise(
            workout=cardio_session,
            exercise=running,
            duration_seconds=1800
        )
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()
    print("✅ Database seeded successfully!")