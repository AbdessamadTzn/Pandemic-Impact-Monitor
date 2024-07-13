# test_app.py
import pytest
from ..src.pages import page2


@pytest.fixture
def client():
    """Create a Dash test client."""
    return app.test_client()

def test_layout(client):
    """Test the layout of the app."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Select Year:' in response.data
    assert b'Select Country:' in response.data

def test_callback(client):
    """Test the callback function."""
    response = client.post('/', data={'year-dropdown': 2020, 'country-dropdown': 'Canada'})
    assert response.status_code == 200
    assert b'Unemployment Rate for Canada in 2020' in response.data
