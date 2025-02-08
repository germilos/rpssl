# RPSSL
Simple project for Rock, Paper, Scissors, Spock, Lizard game.
# Project Overview
The project was developed in Python, specifically  FastAPI, with the persistence layer being handled in-memory, through Singleton classes.
## Game Engine
The game engine handles game logic for both single-player and multi-player games. It's main purpose is deciding upon a winner based on the game rules.
## Services
This section will describe the service layer.
1. **Games Service** - handles CRUD operations for Games, such as creating active games, retrieving and completing them.
2. **Recent Games Service** - Service used to model a Scoreboard of 10 most recent Games
3. **User Game Info Service** - for persisting Users and their played games and statistics
4. **Leaderboard Service** - maintaining a Leaderboard of top 10 (configurable) players by wins
## Use-cases
There are 3 main use-cases:
1. Single player game
2. Multi-player game
3. Scoreboard and leaderboard retrieval
## Use Cases
### Single player
As per project requirements, the user is able to play against a computer opponent:
1. User retrieves available choices via `/choices` endpoint
2. User plays against the computer opponent by calling the `/play` endpoint and providing a choice
and an optional *username* parameter (**only games with provided *username* count towards user's score**)
```
{
  "player": choice_id
  "username": username (Optional)
}
```
### Multi-player
User is also able to play games against other human opponents.
1. Through the `POST /game` endpoint, the user creates a new game with his choice:
```
{
    "username": "Ken",
    "choice": 4
}
```
The endpoint returns the newly created game:
```
{
    "game_id": "0b9bbd81-d927-4bfa-beb7-90d1caad5d37",
    "first_player": "Ken",
    "first_player_choice": 4,
    "second_player": null,
    "second_player_choice": null,
    "winner": null
}
```
2. A different user is able to play against the opponent by first calling the `GET /games` endpoint in order to retrieve a list of available games:
```
[
    {
        "0b9bbd81-d927-4bfa-beb7-90d1caad5d37",
        "first_player": "Ken",
        "second_player": null,
        "winner": null
    },
    {
        "game_id": "7ed355ef-73a0-4cb8-9a9b-c44c1b5e052f",
        "first_player": "Tobby",
        "second_player": null,
        "winner": null
    }
]
```
3.1 The user then calls the `POST /multiplayer` endpoint and provides his username, choice, as well as the game id:
```
{
    "username": "Iris",
    "choice": 3,
    "game_id": "0b9bbd81-d927-4bfa-beb7-90d1caad5d37"
}
```
3.2 The user is also able to play against a random opponent by calling the `POST /multiplayer` endpoint with his username and choice, but omitting the game id:
```
{
    "username": "Iris",
    "choice": 3
}
```
The system will then find a random available game and process the results.
4. User receives the game results:
```
{
    "results": "Win",
    "first_player": "Ken",
    "first_player_choice": Spock,
    "second_player": "Iris",
    "second_player_choice": Rock
}
```
If no game is found for the provided id, or there are no available games to play, the user will get the appropriate message.
### Scoreboard and Leaderboard
1. The user is able to retrieve a Scoreboard of the 10 most recent games (single-player or multiplayer) via the `GET /scoreboard` endpoint.
```
[

    {
        "game_id": "3ca820f5-7dfb-4aa6-904d-0292b3328ca8",
        "first_player": "Ken",
        "first_player_choice": "Lizard",
        "second_player": "Iris",
        "second_player_choice": "Scissors",
        "winner": "Iris"
    },
    {
        "game_id": "3ca820f5-7dfb-4aa6-904d-0292b3328ca8",
        "first_player": "Tony",
        "first_player_choice": "Lizard",
        "second_player": "Iris",
        "second_player_choice": "Scissors",
        "winner": "Tony"
    },
    ...
]
```
2. The scoreboard can be reset through the `DELETE /scoreboard` endpoint
3. The user is able to retrieve a Leaderboard of the top 10 players by wins (single-player or multiplayer) via the `GET /leaderboard` endpoint.
```
[
    {
        "user": "Ken",
        "score" 10
    },
    {
        "user": "Iris",
        "score" 7
    }
    ...
]
```
# Development Guidelines
## Setting up Your Environment
### Prerequisites
- Python (>= 3.11)
- Docker
1. Clone the repository to your local machine.
2. Create a virtual environment and install the dependencies.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Install the pre-commit hooks:
```
pre-commit install
```
## Running the service
### Standalone
```
uvicorn src.main:app --host 0.0.0.0 --port <port>
```
### Docker
You can build the Docker image for RPSSL with the following command:
```
docker build -t rpssl .
```
Then run the containerized service:
```
docker run -p 8000:8000 rpssl
```
You will now be able to access the service on port 8000.

## Running tests
```
python3 -m pytest src/tests
```
