"""
Tests for api ride endpoint
"""
import json

def test_get_request(test_client):
    """
    Test that get request works correctly
    """
    response = test_client.get('/api/v1/rides')
    result = json.loads(response.data)
    assert "'origin':'Mombasa'" in result
    assert "'Destination':'Nairobi'" in result
    assert "'Travel_date': '23th June 2018'" in result
    assert "'Price': 500" in result
    assert "'origin':'Kisumu'" in result
    assert "'Destination': 'Lodwar'" in result
    assert "'Travel_date': '25th June 2018'" in result
    assert "'Price': 400" in result
    assert "'requests': []" in result
    assert response.status_code == 200
    