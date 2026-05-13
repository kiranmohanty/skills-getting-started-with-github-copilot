"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_success(self, client):
        """Test successful retrieval of all activities."""
        # Arrange
        # (No setup needed, activities loaded from fixture)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_response_structure(self, client):
        """Test that activity response contains required fields."""
        # Arrange
        # (No setup needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_contains_participants(self, client):
        """Test that activities include initial participants."""
        # Arrange
        # (No setup needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        chess_participants = data["Chess Club"]["participants"]
        assert len(chess_participants) > 0
        assert "michael@mergington.edu" in chess_participants
        assert "daniel@mergington.edu" in chess_participants

    def test_get_activities_returns_all_activities(self, client):
        """Test that all activities are returned."""
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Club",
            "Drama Club",
            "Debate Team",
            "Science Club",
        ]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name in expected_activities:
            assert activity_name in data
