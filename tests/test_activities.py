"""
Integration tests for the GET /activities endpoint.
Tests retrieving the list of all extracurricular activities.
"""
import pytest


def test_activities_returns_all_activities(client):
    """Test that GET /activities returns all 9 activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 9


def test_activities_response_structure(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activities_have_participants(client):
    """Test that activities contain the expected initial participants"""
    response = client.get("/activities")
    activities = response.json()
    
    # Each activity should have at least one participant initially
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list)
        assert len(activity_data["participants"]) >= 1


def test_activities_specific_activity_exists(client):
    """Test that specific expected activities exist"""
    response = client.get("/activities")
    activities = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Basketball Team",
        "Math Olympiad"
    ]
    
    for activity in expected_activities:
        assert activity in activities
