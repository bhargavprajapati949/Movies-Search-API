
from os import abort
from urllib.parse import urlencode
from flask import escape, jsonify, request
from flask_expects_json import expects_json
from flask_jwt_extended import jwt_required

from main import app
from movie.utils import addMovieReqSchema, addBatchMovieReqSchema, check_numeric, updateMovieReqSchema, deleteMovieReqSchema, searchMovieReqSchema
from movie.modal import Movie
from user.routes import admin_role_required


@app.route('/movie/add', methods=["POST"])
@jwt_required()
@admin_role_required
@expects_json(addMovieReqSchema)
def add_movie():
    data = request.get_json()

    movie = Movie.add_movie(data)
    return movie.json_val, 201    

@app.route('/movie/addBatch', methods=["POST"])
@jwt_required()
@admin_role_required
@expects_json(addBatchMovieReqSchema)
def add_movie_batch():
    data = request.get_json()
    
    Movie.add_batch_movie(data)
    return {"data": data}, 201


@app.route('/movie/update', methods=['PUT'])
@jwt_required()
@admin_role_required
@expects_json(updateMovieReqSchema)
def update_movie():
    data = request.get_json()

    movie_id = data.get('movie_id')
    del data['movie_id']

    Movie.update_movie(movie_id, data)
    
    return {
        'message': 'movie updated'
    }, 200


@app.route('/movie/delete', methods=['DELETE'])
@jwt_required()
@admin_role_required
@expects_json(deleteMovieReqSchema)
def delete_movie():
    
    data = request.get_json()

    movie_id = data.get('movie_id')

    if Movie.get_movie_by_id(movie_id):

        Movie.delete_movie(movie_id)
        return {
            "message": "Movie Deleted"
        }, 200


@app.route('/movie/<movie_id>', methods=["GET"])
def movies(movie_id):
    return Movie.get_movie_by_id(movie_id).json_val, 200


@app.route('/movie', methods=['GET'])
def search_movie():
    
    limit = request.args.get('limit')
    if limit and limit.isdigit():
        limit = int(limit)
        
    # offset = request.args.get('offset')
    # if offset and offset.isdigit():
    #     offset = int(offset)
    # else:
    #     offset = 0
    
    # sort filter will consider only first arg
    sort_by_attr = request.args.get('sort_by_attr')
    if request.args.get('sort_by_order') == 'descending':
        sort_by_order = 'desc'
    else:
        sort_by_order = 'ase'

    name = request.args.get('name')

    director = request.args.get('director')

    if request.args.get('genre_filter_operator') == 'and':
        genre_filter_operator = 'and'
    else:
        genre_filter_operator = 'or'
    
    genre_to_filter = request.args.getlist('genre_to_filter')

    popularity_min = request.args.get('popularity_min')
    if popularity_min and check_numeric(popularity_min):
            popularity_min = float(popularity_min)
    popularity_max = request.args.get('popularity_max')
    if popularity_max and check_numeric(popularity_max):
            popularity_max = float(popularity_max)

    imdb_score_min = request.args.get('imdb_score_min')
    if imdb_score_min and check_numeric(imdb_score_min):
            imdb_score_min = float(imdb_score_min)
    imdb_score_max = request.args.get('imdb_score_max')
    if imdb_score_max and check_numeric(imdb_score_max):
            imdb_score_max = float(imdb_score_max)
    
    query_parm = {}
    query_parm['limit'] = limit
    # query_parm['offset'] = offset
    if sort_by_attr:
        query_parm['sort_by_attr'] = sort_by_attr
    query_parm['sort_by_order'] = sort_by_order
    if name:
        query_parm['name'] = name
    if director:
        query_parm['director'] = director
    if genre_to_filter:
        query_parm['genre_to_filter'] = genre_to_filter
        query_parm['genre_filter_operator'] = genre_filter_operator
    if popularity_min:
        query_parm['popularity_min'] = popularity_min
    if popularity_max:
        query_parm['popularity_max'] = popularity_max
    if imdb_score_min:
        query_parm['imdb_score_min'] = imdb_score_min
    if imdb_score_max:
        query_parm['imdb_score_max'] = imdb_score_max

    res = {}
    res['result'] = Movie.search_movie(query_parm)

    if res['result']:
        pass
        # args = request.args.copy()
        
        # if offset is not 0:
        #     args['offset']
        #     res['prev_url'] = '{}?{}'.format(request.path, urlencode(args))

        # res['next_url'] = request.url
    else:
        del res['result']
        res['message'] = 'No Result Found. Try another query'

    return res, 200