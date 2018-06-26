"""
Api V2 Rides implementation
"""

from apiV2 import app

@app.route('/rides', methods=['GET', 'POST'] )
def rides():
    """
    get all rides
    """
    pass

@app.route('/rides/<int:ride_id>', methods=['GET', 'PUT', 'DELETE'] )
def get_ride(ride_id):
    """
    Get a single ride
    """
    pass