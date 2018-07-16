

  
# Bowling  API
For Freeletics coding challenge.

## Scoring
Scoring is based on ten-pin bowling. 
[https://en.wikipedia.org/wiki/Ten-pin_bowling#Scoring](https://en.wikipedia.org/wiki/Ten-pin_bowling#Scoring)

## Setup

To run, first install the requirements in requirements.txt:

	pip install -r requirements.txt

Create the database and run the server:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Models
`Frame`: Each frame represents a turn (1-3 throws, where 3 throws is only possible in the last frame) and must be associated with a game. This model is not accessed directly, but rather indirectly through the `Game` model.

`Game`: Each game consists of 10 frames. The primary key for each Game is an auto-incrementing key `gameId`.

## API Endpoints

`/admin/`
Built-in Django admin page

`/games/`
 - **GET**: list all games
	- **arguments**: None
	 - **returns**: list of Games including their gameId, whether it is ongoing (gameOver), and the current score.
 
`/games/create/` 
 - **GET**: create a new game
	 - **arguments**: None
	 - **returns**: a new Game with a gameId (int)
	 -  **HTTP responses**:
		 - (successful) HTTP Response: 201 CREATED

Note: This is a `GET` request rather than a `POST` request to the `/games/` endpoint because there are no parameters to creating a new game and you are getting a gameId from calling the endpoint.

 `/games/{gameId}/`
  - **GET**: get game by gameId
	 - **arguments**: None
	 - **returns**: A Game associated with the gameId
	- **HTTP responses**:
		 - (successful) HTTP Response: 200 OK
		 - (unsuccessful) HTTP Response: 400 BAD REQUEST
  
Note: The third throw in the last frame is not shown, but does exist and will update accordingly. 

  - **POST**: updates score of the current game
	 - **arguments**: 
		 - score (int)
	 - **returns**: None
	 - **example**: {"score": 5}
	 - **HTTP responses**:
		 - (successful) HTTP Response: 200 OK
		 - (unsuccessful) HTTP Response: 400 BAD REQUEST

Note: the arguments are in JSON format
