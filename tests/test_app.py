import copy
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def setup_function():
    # Arrange: preserve the current activities state
    global _saved_activities
    _saved_activities = copy.deepcopy(activities)


def teardown_function():
    # Restore original state
    activities.clear()
    activities.update(_saved_activities)


def test_get_activities_works():
    # Act
    response = client.get('/activities')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_new_student_succeeds():
    # Arrange
    email = 'aaa@mergington.edu'

    # Act
    response = client.post('/activities/Chess Club/signup', params={'email': email})

    # Assert
    assert response.status_code == 200
    assert email in activities['Chess Club']['participants']


def test_signup_duplicate_returns_400():
    # Arrange
    email = 'michael@mergington.edu'

    # Act
    response = client.post('/activities/Chess Club/signup', params={'email': email})

    # Assert
    assert response.status_code == 400
    assert 'already signed up' in response.json()['detail']


def test_unregister_student_succeeds():
    # Arrange
    email = 'remove@mergington.edu'
    client.post('/activities/Chess Club/signup', params={'email': email})

    # Act
    response = client.delete('/activities/Chess Club/signup', params={'email': email})

    # Assert
    assert response.status_code == 200
    assert email not in activities['Chess Club']['participants']


def test_unregister_nonexistent_returns_400():
    # Arrange
    email = 'missing@mergington.edu'

    # Act
    response = client.delete('/activities/Chess Club/signup', params={'email': email})

    # Assert
    assert response.status_code == 400
    assert 'not signed up' in response.json()['detail']
