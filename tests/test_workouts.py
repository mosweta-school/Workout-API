import json


def test_get_workouts(client):

    response = client.get("/workouts")

    assert response.status_code == 200

    assert isinstance(response.get_json(), list)


def test_get_single_workout(client):

    response = client.get("/workouts/1")

    assert response.status_code == 200

    workout = response.get_json()

    assert "id" in workout
    assert "date" in workout
    assert "duration_minutes" in workout


def test_get_invalid_workout(client):

    response = client.get("/workouts/9999")

    assert response.status_code == 404


def test_create_workout(client):

    payload = {
        "date": "2026-07-27",
        "duration_minutes": 45,
        "notes": "Pytest Workout"
    }

    response = client.post(
        "/workouts",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 201

    workout = response.get_json()

    assert workout["duration_minutes"] == 45

    assert workout["notes"] == "Pytest Workout"


def test_create_invalid_workout(client):

    payload = {
        "date": "2026-07-27",
        "duration_minutes": -20,
        "notes": "Invalid Workout"
    }

    response = client.post(
        "/workouts",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 400

def test_delete_workout(client):
    """
    Create a workout and then delete it.
    """

    payload = {
        "date": "2026-07-27",
        "duration_minutes": 30,
        "notes": "Delete Me"
    }

    create_response = client.post(
        "/workouts",
        json=payload
    )

    assert create_response.status_code == 201

    workout = create_response.get_json()

    response = client.delete(
        f"/workouts/{workout['id']}"
    )

    assert response.status_code == 200

    assert response.get_json()["message"] == "Workout deleted successfully."


def test_delete_nonexistent_workout(client):
    """
    Deleting a workout that doesn't exist should return 404.
    """

    response = client.delete("/workouts/99999")

    assert response.status_code == 404

    assert response.get_json()["error"] == "Workout not found."