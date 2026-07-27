def test_add_exercise_to_workout(client):

    payload = {
        "sets": 3,
        "reps": 12,
        "duration_seconds": None
    }

    response = client.post(
        "/workouts/3/exercises/1/workout_exercises",
        json=payload
    )

    print("\nStatus:", response.status_code)
    print("Body:", response.get_json())

    assert response.status_code == 201

def test_add_to_invalid_workout(client):

    payload = {
        "sets": 3,
        "reps": 12
    }

    response = client.post(
        "/workouts/999/exercises/1/workout_exercises",
        json=payload
    )

    assert response.status_code == 404

    assert response.get_json()["error"] == "Workout not found."

def test_add_invalid_exercise(client):

    payload = {
        "sets": 3,
        "reps": 12
    }

    response = client.post(
        "/workouts/1/exercises/999/workout_exercises",
        json=payload
    )

    assert response.status_code == 404

    assert response.get_json()["error"] == "Exercise not found."

def test_duplicate_workout_exercise(client):

    payload = {
        "sets": 3,
        "reps": 12
    }

    client.post(
        "/workouts/1/exercises/2/workout_exercises",
        json=payload
    )

    response = client.post(
        "/workouts/1/exercises/2/workout_exercises",
        json=payload
    )

    assert response.status_code == 400

    assert response.get_json()["error"] == (
        "Exercise already exists in this workout."
    )

def test_invalid_reps(client):

    payload = {
        "sets": 3,
        "reps": -10
    }

    response = client.post(
        "/workouts/1/exercises/2/workout_exercises",
        json=payload
    )

    assert response.status_code == 400

def test_invalid_sets(client):

    payload = {
        "sets": -2,
        "reps": 12
    }

    response = client.post(
        "/workouts/1/exercises/2/workout_exercises",
        json=payload
    )

    assert response.status_code == 400

def test_invalid_duration(client):

    payload = {
        "duration_seconds": -60
    }

    response = client.post(
        "/workouts/1/exercises/2/workout_exercises",
        json=payload
    )

    assert response.status_code == 400