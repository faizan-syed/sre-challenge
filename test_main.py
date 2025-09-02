from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "version" in data


def test_read_item():
    """Test reading an item without query parameter"""
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": None}


def test_read_item_with_query():
    """Test reading an item with query parameter"""
    response = client.get("/items/42?q=testing")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "testing"}


def test_read_item_negative_id():
    """Test reading an item with negative ID should fail"""
    response = client.get("/items/-1")
    assert response.status_code == 400
    assert "Item ID must be positive" in response.json()["detail"]


def test_update_item():
    """Test updating an item"""
    data = {"name": "Test Item", "price": 19.99, "is_offer": True}
    response = client.put("/items/42", json=data)
    assert response.status_code == 200
    assert response.json() == {"item_name": "Test Item", "item_id": 42}


def test_update_item_negative_id():
    """Test updating an item with negative ID should fail"""
    data = {"name": "Test Item", "price": 19.99, "is_offer": True}
    response = client.put("/items/-1", json=data)
    assert response.status_code == 400
    assert "Item ID must be positive" in response.json()["detail"]


def test_data_endpoint():
    """Test the data endpoint"""
    response = client.get("/data")
    assert response.status_code == 200
    data = response.json()

    # Check that all expected keys are present
    expected_keys = [
        "DB_PASSWORD",
        "API_BASE_URL",
        "LOG_LEVEL",
        "MAX_CONNECTIONS",
        "ENVIRONMENT",
    ]
    for key in expected_keys:
        assert key in data

    # Check that DB_PASSWORD is masked for security
    if data["DB_PASSWORD"] is not None:
        assert data["DB_PASSWORD"] == "***"
