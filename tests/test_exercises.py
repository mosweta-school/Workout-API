
def test_get_exercises(client):
    """
    Test GET /exercises
    """

    response = client.get("/exercises")

    assert response.status_code == 200

    assert isinstance(response.get_json(), list)

def test_get_exercises(client):

    response = client.get("/exercises")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_single_exercise(client):

    response = client.get("/exercises/1")

    assert response.status_code == 200

    exercise = response.get_json()

    assert "id" in exercise
    assert "name" in exercise
    assert "category" in exercise
    assert "equipment_needed" in exercise


def test_get_invalid_exercise(client):

    response = client.get("/exercises/99999")

    assert response.status_code == 404

    assert response.get_json()["error"] == "Exercise not found."

def test_create_exercise(client):

    payload = {
        "name": "Bench Press 8",
        "category": "Strength",
        "equipment_needed": True
    }

    response = client.post(
        "/exercises",
        json=payload
    )

    assert response.status_code == 201

    exercise = response.get_json()

    assert exercise["name"] == payload["name"]
    assert exercise["category"] == payload["category"]
    assert exercise["equipment_needed"] == payload["equipment_needed"]


def test_create_invalid_exercise(client):

    payload = {
        "name": "Romanian Deadlift Test",
        "category": "Swimming",
        "equipment_needed": True
    }

    response = client.post(
        "/exercises",
        json=payload
    )

    assert response.status_code == 400

def test_delete_exercise(client):
    payload = {
        "name": "Burpees Test",
        "category": "Cardio",
        "equipment_needed": False
    }

    create_response = client.post("/exercises", json=payload)
    assert create_response.status_code == 201

    exercise = create_response.get_json()

    response = client.delete(f"/exercises/{exercise['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Exercise deleted successfully."


def test_delete_nonexistent_exercise(client):
    response = client.delete("/exercises/99999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Exercise not found."