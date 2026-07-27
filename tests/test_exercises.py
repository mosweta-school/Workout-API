
def test_get_exercises(client):
    """
    Test GET /exercises
    """

    response = client.get("/exercises")

    assert response.status_code == 200

    assert isinstance(response.get_json(), list)