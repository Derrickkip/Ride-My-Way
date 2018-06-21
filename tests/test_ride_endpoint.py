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
    print(result)
    assert result['rides'][0]['origin'] == 'Mombasa'
    assert result['rides'][0]['destination'] == 'Nairobi'
    assert result['rides'][0]['Travel_date'] == '23th June 2018'
    assert result['rides'][0]['Time'] == '10:00 am' 
    assert result['rides'][0]['price'] == 500
    assert result['rides'][0]['requests'] == []
    assert result['rides'][1]['origin'] == 'Kisumu'
    assert result['rides'][1]['destination'] == 'Lodwar'
    assert result['rides'][1]['Travel_date'] == '25th June 2018'
    assert result['rides'][1]['Time'] == '12:00 am'
    assert result['rides'][1]['price'] == 400
    assert result['rides'][1]['requests'] == []
    assert response.status_code == 200
    