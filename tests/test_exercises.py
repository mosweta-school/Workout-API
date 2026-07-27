
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