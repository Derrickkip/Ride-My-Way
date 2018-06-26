[![Build Status](https://travis-ci.org/Derrickkip/Ride-My-Way.svg?branch=develop)](https://travis-ci.org/Derrickkip/Ride-My-Way) [![Coverage Status](https://coveralls.io/repos/github/Derrickkip/Ride-My-Way/badge.svg?branch=develop)](https://coveralls.io/github/Derrickkip/Ride-My-Way?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/b3f10d58926db9638e30/maintainability)](https://codeclimate.com/github/Derrickkip/Ride-My-Way/maintainability)

# RIDE-MY-WAY
 Ride-My-Way is a carpooling app that allows drivers to create ride offers and passengers to join available ride offers
 
## FEATURES
* Users can create accounts and Sign In
* Drivers can create rides
* Passengers can view available rides offers
* Passengers can request to join a ride
* Drivers can accept or reject requests to rides they created

## Getting started
 Ride-My-Way is written in python using the Flask framework
### Requirements
To get started you need the following
 * Git
 * Python3

### Installation
1. To clone this repo run ``git clone https://github.com/Derrickkip/Ride-My-Way.git`` from your local terminal
2. Cd into the Ride-My-Way Folders
3. Create a virtual environment `python3 -m venv venv`
4. Activate the virtual environment `source venv/bin/activate`
5. Install requirements `pip install -r requirements.txt` This should install all dependancies including flask
5. Now Run the app `python run.py`

### Usage
The api Implements a CRUD interface for rides and users using GET, POST, PUT and DELETE HTTP methods

#### CREATE
run `curl -i -H "Content-Type: application/json" -X POST -d '{"origin":"Kitui", "destination":"Kitale", "travel_date": "25th June 2018", "time": "11:00 pm", "driver": "Simon Mbugua", "car_model": "subaru Impreza", "seats":3, "price": 200}' http://localhost:5000/api/v1/rides` to create a new ride
Then test that its working by running a get request again `curl -i http://localhost:5000/api/v1/rides`

#### READ
run `curl -i http://localhost:5000/api/v1/rides` to test the rides endpoint from another terminal. Should return an empty dictionary

#### UPDATE
Now that a ride has been created we can edit the ride
to edit run `curl -i -H "Content-Type: application/json" -X PUT -d '{"origin":"Nairobi", "destination":"Mombasa", "travel_date": "25th August 2018", "time": "01:00 pm"}' http://localhost:5000/api/v1/rides/1`

#### DELETE
You can delete the ride by running `curl -i -X DELETE http://localhost:5000/api/v1/rides/1` 

Alternatively you can use POSTMAN to test the endpoints. POSTMAN offers a nice interface and is easy to use.

Here is a screenshot from postman

![Alt postman](/screenshots/postman.png)




## Author
* [Derrick Kipkirui](https://github.com/Derrickkip)

## Acknowledgements
* [Micah Oriaso](https://github.com/micahoriaso)  for his valuable insights


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
