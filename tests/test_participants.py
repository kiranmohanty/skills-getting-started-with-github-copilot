"""Tests for the DELETE /activities/{activity_name}/participants endpoint."""

import pytest


class TestUnregisterParticipant:
    """Test suite for participant removal functionality."""

    def test_unregister_success(self, client):
        """Test successful removal of a participant from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_participant(self, client):
        """Test that removing a non-registered participant fails."""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]

    def test_unregister_nonexistent_activity(self, client):
        """Test that removing a participant from nonexistent activity fails."""
        # Arrange
        activity_name = "Fake Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_unregister_twice_fails(self, client):
        """Test that unregistering the same participant twice fails."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response1 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        response2 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404

    def test_unregister_then_signup(self, client):
        """Test that a participant can re-signup after unregistering."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        # Unregister
        response1 = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        # Sign up again
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]
