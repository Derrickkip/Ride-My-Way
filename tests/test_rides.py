"""
Tests for api ride endpoint
"""
import json

def create_ride(test_client, data):
    """
    Helper Function to create ride to be tested
    """
    my_data = data

    response = test_client.post('/api/v1/rides', data=json.dumps(my_data),
                                content_type='application/json')

    return response

def test_create_ride(test_client):
    """
    Test that a ride is successfuly created
    """
    my_data = {'driver':'Michael Owen', 'origin':'Mombasa', 'destination': 'Nairobi',
               'travel_date': '23rd June 2018',
               'time': '10:00 am', 'car_model': 'Mitsubishi Evo 8', 'seats': 4, 'price' : 500}
    response = create_ride(test_client, my_data)
    assert response.status_code == 201

def test_create_with_empty_value(test_client):
    """
    Should raise a 400 error if the vaalue of a key is empty
    """
    my_data = {'driver':'', 'origin':'Mombasa', 'destination': 'Nairobi',
               'travel_date': '23rd June 2018',
               'time': '10:00 am', 'car_model': 'Mitsubishi Evo 8', 'seats': 4, 'price' : 500}

    response = create_ride(test_client, my_data)

    assert response.status_code == 400

def test_get_rides(test_client):
    """
    Test that get request works correctly
    """
    response = test_client.get('/api/v1/rides')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert len(result['rides']) == 1

def test_get_single_ride(test_client):
    """
    Test request returns correct ride with specified ID
    """
    my_data = {'driver':'Michael Owen', 'origin':'Mombasa', 'destination': 'Nairobi',
               'travel_date': '23rd June 2018',
               'time': '10:00 am', 'car_model': 'Mitsubishi Evo 8', 'seats': 4, 'price' : 500}
    response1 = create_ride(test_client, my_data)
    assert response1.status_code == 201
    response = test_client.get('/api/v1/rides/1')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['ride']['driver'] == 'Michael Owen'
    assert result['ride']['origin'] == 'Mombasa'
    assert result['ride']['destination'] == 'Nairobi'
    assert result['ride']['travel_date'] == '23rd June 2018'
    assert result['ride']['time'] == '10:00 am'
    assert result['ride']['car_model'] == 'Mitsubishi Evo 8'
    assert result['ride']['seats'] == 4
    assert result['ride']['price'] == 500
    assert result['ride']['requests'] == []

def test_get_unavailable_ride(test_client):
    """
    Test request returns a 404 error if ride is not present
    """
    response = test_client.get('/api/v1/rides/4')
    assert response.status_code == 404

def test_missing_field(test_client):
    """
    Test returns 404 error if driver is not included in request
    """
    my_data = {'origin':'Londiani', 'destination': 'Brooke', 'travel_date': '30th August 2018',
               'time': '03:00 pm', 'car_model': 'Range Rover Sport', 'seats': 5, 'price' : 200}

    response = test_client.post('/api/v1/rides', data=json.dumps(my_data),
                                content_type='application/json')

    assert response.status_code == 400

def test_update_ride(test_client):
    """
    Test A ride can be updated
    """
    my_data = {'destination': 'Brooke', 'time': '03:00 pm', 'price' : 2000}
    response = test_client.put('/api/v1/rides/1', data=json.dumps(my_data),
                               content_type='application/json')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['ride']['driver'] == 'Michael Owen'
    assert result['ride']['origin'] == 'Mombasa'
    assert result['ride']['destination'] == 'Brooke'
    assert result['ride']['travel_date'] == '23rd June 2018'
    assert result['ride']['time'] == '03:00 pm'
    assert result['ride']['car_model'] == 'Mitsubishi Evo 8'
    assert result['ride']['seats'] == 4
    assert result['ride']['price'] == 2000

def test_update_ride_without_values(test_client):
    """
    Should return a 400 error
    """
    my_data = {'destination': ""}
    response = test_client.put('/api/v1/rides/1', data=json.dumps(my_data),
                               content_type='application/json')

    assert response.status_code == 400

def test_get_requests(test_client):
    """
    Test get all requests to ride with ride_id
    """
    response = test_client.get('/api/v1/rides/1/requests')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['requests'] == []

def test_make_requests(test_client):
    """
    Test make request to ride with ride_id
    """
    my_data = {'username':'Meek Mill'}
    response = test_client.post('/api/v1/rides/1/requests', data=json.dumps(my_data),
                                content_type='application/json')
    assert response.status_code == 201
    result = json.loads(response.data)
    assert result['requests'][0]['username'] == 'Meek Mill'

def test_make_bad_requests(test_client):
    """
    Should return 400 error when data is not valid
    """
    my_data = {'username':''}
    response = test_client.post('/api/v1/rides/1/requests', data=json.dumps(my_data),
                                content_type='application/json')
    assert response.status_code == 400

def test_delete_ride(test_client):
    """
    Test A ride can be deleted with the delete method
    """
    response = test_client.delete('/api/v1/rides/1')
    assert response.status_code == 204
