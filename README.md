# FSND-capstone-project


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.y` directs flask to use the `app.py` file to find the application. 


Endpoints
GET '/movies'
GET '/movies/<int:movie_id>'
GET '/actors'
GET '/actors/<int:actor_id>'
POST '/movies'
POST '/actors'
DELETE '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'
PATCH '/actors/<int:actor_id>'

GET '/movies'
- Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding object of the movie
- Request Arguments: None
- Return : list of movies objects
{
    "movies": [
        {
            "id": 1,
            "release_date": null,
            "title": "Avater 2"
        },
        {
            "id": 2,
            "release_date": null,
            "title": "Taken"
        },
        {
            "id": 4,
            "release_date": null,
            "title": "her"
        },
        {
            "id": 5,
            "release_date": null,
            "title": "her"
        }
    ],
    "success": true,
    "total_movies": 4
}

GET /movies/2
- fetches one moive detials
- Request Arguments: None
- Returns: An object consist of id, release_date and title of movie.

{
    "movie": {
        "id": 2,
        "release_date": null,
        "title": "Taken"
    },
    "success": true
}

GET '/actors'
- Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding object of the actor
- Request Arguments: None
- Return : list of acotrs objects

{
    "actors": [
        {
            "age": 22,
            "gender": false,
            "id": 2,
            "name": "alaa"
        },
        {
            "age": 26,
            "gender": true,
            "id": 3,
            "name": "ali"
        }
    ],
    "success": true,
    "total_actors": 2
}


GET /actors/2
- fetches one actor detials
- Request Arguments: None
- Returns: An object consist of id, name, age and gender of actor.

{
    "actor": {
        "age": 22,
        "gender": false,
        "id": 2,
        "name": "alaa"
    },
    "success": true
}


POST '/movies'
- Create new movie via send json object constains of title and release_date of movie.

POST '/actors'
- Create new actor via send json object constains of name, age and gender of actor.

DELETE '/movies/<int:movie_id>'
- Delete movie with gevin movie_id

DELETE '/actors/<int:actor_id>'
- Delete actor with gevin actor_id


PATCH '/movies/<int:movie_id>'
- Update movie via send json object constains of title and release_date of movie.

PATCH '/actors/<int:actor_id>'
- Update actor via send json object constains of name, age and gender of actor.

## Testing
To run the tests, run
```
make copy of "database.db" file and rename it to "test_database.db" then
python test_app.py
```