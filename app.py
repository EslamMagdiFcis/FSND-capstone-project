from operator import ge
from flask import Flask, request, abort, jsonify
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Actor, Movie, setup_db, db_drop_and_create_all
from auth.auth import requires_auth, AuthError


ELEMENTS_PER_PAGE = 10


def paginate_elements(request, elements):
  page = request.args.get('page', 1, type=int)
  elements_json = [element.format() for element in elements]
  start_index = (page - 1)  * ELEMENTS_PER_PAGE
  end_index = start_index + ELEMENTS_PER_PAGE

  return elements_json[start_index:end_index]


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth(permission='read:movies')
  def read_movie(_, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
      AuthError(404, 404)

    return jsonify({
      "success": True, 
      "movie": movie.format()
      })


  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth(permission='delete:movies')
  def delete_movie(_, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        AuthError(404, 404)

      movie.delete()
      selection = Movie.query.order_by(Movie.id).all()
      current_movies = paginate_elements(request, selection)

      return jsonify({
        'success': True,
        'deleted': movie_id,
        'movies': current_movies,
        'total_movies': len(Movie.query.all())
      })

    except:
      AuthError(422, 422)


  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth(permission='patch:movies')
  def edit_movie(_, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
      AuthError(404, 404)
    
    body = request.get_json()

    movie.title = body.get('title', None)
    movie.release_date = body.get('release_date', None)

    movie.update()

    return jsonify({
      "success": True, 
      "movie": movie.format()
      })


  @app.route('/movies', methods=['POST'])
  @requires_auth(permission='post:movies')
  def create_movie(_):
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    movie = Movie(title, release_date)

    movie.insert()
    
    return jsonify({
        "success": True, 
        "movie": movie.format()
        })

  
  @app.route('/movies')
  @requires_auth(permission='read:movies')
  def movies_list(_):
    movies = Movie.query.order_by(Movie.id).all()
    current_movies = paginate_elements(request, movies)

    if len(movies) == 0:
      AuthError(404, 404)

    return jsonify({
      'success': True,
      'movies': current_movies,
      'total_movies': len(current_movies),
    })


  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth(permission='patch:actors')
  def edit_drink(_, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      AuthError(404, 404)
    
    body = request.get_json()

    actor.name = body.get('name', None)
    actor.age = body.get('age', 0)
    actor.gender = body.get('gender', True)

    actor.update()

    return jsonify({
        "success": True, 
        "actor": actor.format()
        })

  
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth(permission='delete:actors')
  def delete_actor(_, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        AuthError(404, 404)

      actor.delete()
      selection = Actor.query.order_by(Actor.id).all()
      current_actors = paginate_elements(request, selection)

      return jsonify({
        'success': True,
        'deleted': actor_id,
        'actors': current_actors,
        'total_actors': len(Actor.query.all())
      })

    except:
      AuthError(422, 422)


  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth(permission='patch:actors')
  def read_actor(_, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      AuthError(404, 404)

    return jsonify({
      "success": True, 
      "actor": actor.format()
      })


  @app.route('/actors', methods=['POST'])
  @requires_auth(permission='post:actors')
  def create_actor(_):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    actor = Actor(name=name, age=age, gender=gender)

    actor.insert()
    
    return jsonify({
        "success": True, 
        "actor": actor.format()
        })


  @app.route('/actors')
  @requires_auth(permission='read:actors')
  def actors_list(_):
    actors = Actor.query.order_by(Actor.id).all()
    current_actors = paginate_elements(request, actors)

    if len(current_actors) == 0:
      AuthError(404, 404)

    return jsonify({
      'success': True,
      'actors': current_actors,
      'total_actors': len(current_actors),
    })


    # # Error Handling
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "unprocessable"
                      }), 422


  @app.errorhandler(404)
  def resource_not_found(error):
    return  jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

  # '''
  #     error handler should confirm to general task above 
  # '''

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


  # db_drop_and_create_all()
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
