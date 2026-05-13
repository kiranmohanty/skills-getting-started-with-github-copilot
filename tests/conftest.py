"""Test configuration and fixtures for FastAPI activity management app."""

import copy
from fastapi.testclient import TestClient
import pytest
from src import app as app_module


# Store the original activities state from first import
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice team soccer skills and play matches against other schools",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "maya@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Develop basketball techniques and scrimmage with classmates",
        "schedule": "Mondays and Wednesdays, 4:30 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and creative art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
    },
    "Drama Club": {
        "description": "Practice acting, stagecraft, and put on school performances",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["chloe@mergington.edu", "jack@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare for debate competitions and improve public speaking",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["amelia@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore science topics with hands-on projects",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["harper@mergington.edu", "elijah@mergington.edu"]
    }
}


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    # Clear and repopulate with fresh copy of original data
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    yield app_module.activities
    
    # Cleanup: restore original state after test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client(reset_activities):
    """Create a test client for the FastAPI app."""
    return TestClient(app_module.app)
