"""
Test ride endpoints
"""
import json

def test_read_rides(test_client):
    """
    Test returns list of rides
    """
    response = test_client.get('api/v2/rides')
    assert response.status_code == 200

def test_read_single_ride(test_client):
    """
    Test get single ride
    """
    response = test_client.get('api/v2/rides/1')
    assert response.status_code == 200

def test_create_ride(test_client):
    """
    test create ride
    """
    my_data = {'driver':'Michael Owen', 'origin':'Mombasa', 'destination': 'Nairobi',
               'travel_date': '23rd June 2018',
               'time': '10:00 am', 'car_model': 'Mitsubishi Evo 8', 'seats': 4, 'price' : 500}
    response = test_client.post('api/v2/rides', data=json.dumps(my_data),
                                 content_type='application/json')
    assert response.status_code == 201

def test_update_ride(test_client):
    """
    test update ride
    """
    my_data = {"travel_date":"30th June 2018" ,"price": 2000}
    response = test_client.put('api/v2/rides', data=json.dumps(my_data),
                                content_type='application/json')
    assert response.status_code == 200

def test_delete_ride(test_client):
    """
    test delete ride
    """
    response = test_client.delete('api/v2/rides/1')
    assert response.status_code == 204
