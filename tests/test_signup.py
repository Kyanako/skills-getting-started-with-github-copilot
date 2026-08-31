"""
Integration tests for the POST /activities/{activity_name}/signup endpoint.
Tests student registration for extracurricular activities.
"""
import pytest


def test_signup_successful(client):
    """Test successful signup adds email to activity participants"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify the student was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_prevention(client):
    """Test that duplicate signup is prevented"""
    activity_name = "Programming Class"
    email = "newstudent2@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_missing_email_parameter(client):
    """Test signup without email parameter returns error"""
    response = client.post("/activities/Chess Club/signup")
    
    # FastAPI should return a validation error (422 Unprocessable Entity)
    assert response.status_code == 422


def test_signup_with_already_registered_student(client):
    """Test signup prevents registering a student who is already registered"""
    activity_name = "Tennis Club"
    # sarah@mergington.edu is already registered in Tennis Club
    email = "sarah@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_multiple_students_same_activity(client):
    """Test multiple students can sign up for the same activity"""
    activity_name = "Drama Club"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    assert response2.status_code == 200
    
    # Verify both are in the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email1 in activities[activity_name]["participants"]
    assert email2 in activities[activity_name]["participants"]
