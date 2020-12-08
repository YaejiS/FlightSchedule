# FlightSchedule App with Airline reviews
### Hosted on https://flight-schedule-app.herokuapp.com/
#

Steps to run on your local machine:
```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
flask run
```

This project uses the following libraries:
- `requests`
- `Flask`
- `Flask-MongoEngine`
- `Flask-Talisman`
- `Flask-WTF`
- `Flask-Bcrypt`
- `Flask-Login`
- `Flask-Mail`
- `python-dotenv`
- `pyotp`

## Search flight
Depart and Arrive input must be a 3-letter, all-capitalized airport code. The 3-letter code could be searched using the search bar included. The search bar takes as an input any city, airport, or State name and return the code of airports nearby.

For an example input, try searching for the following:
```
Depart: IAD
Arrive: LAX
Flight date: 2020-12-28
```
The above input is valid if today's date is before 2020-12-28. Otherwise, pick any date after today.

## Register an account
After you "Sign Up", you will be taken to a 2-factor authentication page. 
A 2-factor authentication app such as DuoMobile is required to register an account and log in in the future. The app is used to provide a verification code each time you log in. If there is an invalid code error, you may need to get a new code.

## Login
Login is required in order to save a flight or leave an airline review. While loggin in, if there is an invalid code error, you may need to get a new code from the app. Once logged in, the user is able to view the saved flights or reviews.

## Leave a review

## Save a flight