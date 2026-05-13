"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for activity signup functionality."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant to the activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_email_fails(self, client):
        """Test that signing up with an already registered email fails."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity(self, client):
        """Test that signing up for a nonexistent activity fails."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]

    def test_signup_multiple_different_activities(self, client):
        """Test that a student can sign up for multiple activities."""
        # Arrange
        email = "multiactivity@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Art Club"]

        # Act
        for activity_name in activities_to_join:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        response = client.get("/activities")
        data = response.json()
        for activity_name in activities_to_join:
            assert email in data[activity_name]["participants"]

    def test_signup_case_sensitive_email(self, client):
        """Test that email comparison is case-sensitive or normalized."""
        # Arrange
        activity_name = "Soccer Team"
        email1 = "test@mergington.edu"
        email2 = "TEST@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )

        # Assert
        # Both should succeed since they are treated as different emails
        assert response1.status_code == 200
        assert response2.status_code == 200
