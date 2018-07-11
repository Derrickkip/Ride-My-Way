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
2. `git checkout develop` to use the develop branch
3. Cd into the Ride-My-Way Folders
4. Create a virtual environment `python3 -m venv venv`
5. Activate the virtual environment `source venv/bin/activate`
6. Install requirements `pip install -r requirements.txt` This should install all dependancies including flask
7. Create a `.env` file
8. Copy the contents of `.env.sample` into `.env`
9. Replace the urls in the env with relevant database urls
10. In the terminal run `source .env` to export the settings
11. Now Run the app `python server.py`

### Usage
The api Implements a CRUD interface for rides using GET, POST, PUT and DELETE HTTP methods. The Api also has an auth route with signup and login

#### Available endpoints
| Method             | Endpoint                                | Functionality
|:------------------:|:---------------------------------------:|:--------------------------------------:|
 POST                | /auth/signup                            | register a new account
 POST                | /auth/login                             | login into application
 GET                 | /rides                                  | get a list of all available ride offers
 GET                 | /rides/<ride_id>                        | get ride with specified ride_id
 POST                | /rides                                  | Create a new ride
 PUT                 | /rides/ride_id>                         | Update ride with specified ride_id
 DELETE              | /rides/<ride_id>                        | Delete ride with specified ride_id
 POST                | /rides/<ride_id>/requests               | Make a request for ride with ride_id
 GET                 | /rides/<ride_id>/requests               | Get all requests to ride with specified ride_id
 PUT                 | /rides/<ride_id>/requests/<requests_id> |respond to a ride request with either accept or reject

The endpoints above can be tested using postman which offers a friendly and easy to use interface.
* NOTE * After logging in an access token is returned that needs to be passed in the header of all the other requests

##Testing
The api tests are written in pytest
To run the tests type `coverage run -m pytest`



## Author
* [Derrick Kipkirui](https://github.com/Derrickkip)

## Acknowledgements
* [Micah Oriaso](https://github.com/micahoriaso)
* My LFA's Millicent and Gidraf 


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
