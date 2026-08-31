"""
Integration tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
Tests student unregistration from extracurricular activities.
"""
import pytest


def test_unregister_successful(client):
    """Test successful unregistration removes email from participants"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # First, sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Verify they were added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]
    
    # Now unregister them
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify they were actually removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_nonexistent_student(client):
    """Test unregistering a student not in the activity returns 400"""
    activity_name = "Basketball Team"
    email = "nonexistent@mergington.edu"
    
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"].lower()


def test_unregister_from_nonexistent_activity(client):
    """Test unregistering from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Activity/participants/student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_updates_participant_count(client):
    """Test that unregistering decreases the participant count"""
    activity_name = "Art Studio"
    email = "teststudent@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Sign up
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Get count after signup
    after_signup_response = client.get("/activities")
    after_signup_count = len(after_signup_response.json()[activity_name]["participants"])
    assert after_signup_count == initial_count + 1
    
    # Unregister
    client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Get count after unregister
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count


def test_unregister_original_participant(client):
    """Test unregistering one of the original participants works"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Original participant
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Unregister original participant
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    assert response.status_code == 200
    
    # Verify removal
    activities_response = client.get("/activities")
    final_count = len(activities_response.json()[activity_name]["participants"])
    assert final_count == initial_count - 1
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_then_signup_again(client):
    """Test that a student can unregister and then sign up again"""
    activity_name = "Debate Team"
    email = "flexible@mergington.edu"
    
    # Sign up
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Unregister
    response2 = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert response2.status_code == 200
    
    # Sign up again
    response3 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response3.status_code == 200
    
    # Verify they're back in the activity
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]
