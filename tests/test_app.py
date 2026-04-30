def test_get_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in data
    assert data[expected_activity]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    signup_url = f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"

    # Act
    response = client.post(signup_url)
    data = response.json()
    participants = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in participants


def test_duplicate_signup_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"
    signup_url = f"/activities/Chess%20Club/signup?email={email}"

    # Act
    response = client.post(signup_url)
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    signup_url = "/activities/Not%20A%20Club/signup?email=test@mergington.edu"

    # Act
    response = client.post(signup_url)
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_remove_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    remove_url = f"/activities/Chess%20Club/participants?email={email}"

    # Act
    response = client.delete(remove_url)
    data = response.json()
    participants = client.get("/activities").json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Removed {email} from Chess Club"
    assert email not in participants


def test_remove_missing_participant_returns_404(client):
    # Arrange
    remove_url = "/activities/Chess%20Club/participants?email=missing@mergington.edu"

    # Act
    response = client.delete(remove_url)
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"
