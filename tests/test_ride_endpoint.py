"""
Tests for api ride endpoint
"""
import json

def test_get_request(test_client):
    """
    Test that get request works correctly
    """
    response = test_client.get('/ridemyway/api/v1/rides')
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
    response = test_client.get('/ridemyway/api/v1/rides/2')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['ride']['origin'] == 'Kisumu'
    assert result['ride']['destination'] == 'Lodwar'
    assert result['ride']['travel_date'] == '25th June 2018'
    assert result['ride']['time'] == '12:00 am'
    assert result['ride']['price'] == 400
    assert result['ride']['requests'] == []

def test_unavailable_ride(test_client):
    """
    Test request returns a 404 error if ride is not present
    """
    response = test_client.get('/ridemyway/api/v1/rides/4')
    assert response.status_code == 404

def test_malformed_request(test_client):
    """
    Test 400 error code raised
    """
    response = test_client.post('/ridemyway/api/v1/rides')
    assert response.status_code == 400

def test_create_ride(test_client):
    """
    Test A new ride is created with the post method
    """
    my_data = {'origin':'Londiani', 'destination': 'Brooke',
               'travel_date': '30th August 2018',
               'time': '03:00 pm', 'price' : 200}

    response = test_client.post('/ridemyway/api/v1/rides', data=json.dumps(my_data),
                                content_type='application/json')
    result = json.loads(response.data)
    assert response.status_code == 201
    assert result['ride']['id'] == 3
    assert result['ride']['origin'] == 'Londiani'
    assert result['ride']['destination'] == 'Brooke'
    assert result['ride']['travel_date'] == '30th August 2018'
    assert result['ride']['time'] == '03:00 pm'
    assert result['ride']['price'] == 200
    assert result['ride']['requests'] == []

def test_update_ride(test_client):
    """
    Test A ride can be updated
    """
    my_data = {'destination': 'Brooke', 'time': '03:00 pm', 'price' : 2000}
    response = test_client.put('/ridemyway/api/v1/rides/1', data=json.dumps(my_data),
                               content_type='application/json')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['ride']['origin'] == 'Mombasa'
    assert result['ride']['destination'] == 'Brooke'
    assert result['ride']['travel_date'] == '23th June 2018'
    assert result['ride']['time'] == '03:00 pm'
    assert result['ride']['price'] == 2000

def test_delete_ride(test_client):
    """
    Test A ride can be deleted with the delete method
    """
    response = test_client.delete('/ridemyway/api/v1/rides/1')
    assert response.status_code == 204
    response2 = test_client.get('/ridemyway/api/v1/rides/1')
    assert response2.status_code == 404
