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
    assert result['rides'][0]['origin'] == 'Mombasa'
    assert result['rides'][0]['destination'] == 'Nairobi'
    assert result['rides'][0]['travel_date'] == '23th June 2018'
    assert result['rides'][0]['time'] == '10:00 am'
    assert result['rides'][0]['price'] == 500
    assert result['rides'][0]['requests'] == []
    assert result['rides'][1]['origin'] == 'Kisumu'
    assert result['rides'][1]['destination'] == 'Lodwar'
    assert result['rides'][1]['travel_date'] == '25th June 2018'
    assert result['rides'][1]['time'] == '12:00 am'
    assert result['rides'][1]['price'] == 400
    assert result['rides'][1]['requests'] == []
    assert response.status_code == 200

def test_get_single_ride(test_client):
    """
    Test request returns correct ride with specified ID
    """
    response = test_client.get('/api/v1/rides/2')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['ride']['origin'] == 'Kisumu'
    assert result['ride']['destination'] == 'Lodwar'
    assert result['ride']['travel_date'] == '25th June 2018'
    assert result['ride']['time'] == '12:00 am'
    assert result['ride']['price'] == 400
    assert result['ride']['requests'] == []
    