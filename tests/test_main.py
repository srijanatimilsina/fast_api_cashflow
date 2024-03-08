import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Accuracy of Calculations
def test_cash_flow_calculation():
    response = client.get("/cash-flow/?start_date=2022-01-01&analysis_type=monthly")
    data = response.json()["cash_flow"]
    assert "operating_cash_flow" in data


# Input Validation
def test_invalid_date_format():
    response = client.get("/cash-flow/?start_date=invalid_date&analysis_type=monthly")
    assert response.status_code == 400
    assert "Invalid date format" in response.text

def test_invalid_analysis_type():
    response = client.get("/cash-flow/?start_date=2022-01-01&analysis_type=invalid_type")
    assert response.status_code == 400
    assert "Invalid analysis type" in response.text

# Performance Testing (assuming you have a larger dataset)
@pytest.mark.large_dataset
def test_large_dataset_performance():
    # Simulate a request with a larger dataset
    response = client.get("/cash-flow/?start_date=2020-01-01&analysis_type=yearly")
    assert response.status_code == 200
