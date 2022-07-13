import re
import pymongo
from database.database import db
from database.common import get_ObjectId_if_valid

movies = db.movies

def add_movie_batch(movies_list):
    return movies.insert_many(movies_list)

def add_movie(movie):
    return movies.insert_one(movie)

def update_movie(movie_id, movie_data_updated):

    genre_query = None
    genre = movie_data_updated.get('genre', None)
    if genre:
        action = genre.get('action')
        if action == 'replaceNew':
            movie_data_updated['genre'] = list(set(movie_data_updated['genre']['data']))
        elif action == 'add':
            genre_query = {
                '$addToSet' : {
                    'genre' : {
                        '$each' : list(set(movie_data_updated['genre']['data']))
                    }
                }
            }
            del movie_data_updated['genre']
        elif action == 'delete':
            genre_query = {
                '$pull': {
                    'genre' : {
                        '$in' : list(set(movie_data_updated['genre']['data']))
                    }
                }
            }
            del movie_data_updated['genre']

    update_query = {"$set" : movie_data_updated}
    if genre_query:
        update_query.update(genre_query)

    print("Now updating")
    return movies.update_one(
        {"_id": get_ObjectId_if_valid(movie_id)},
        update_query
    )

def delete_movie(movie_id):
    obj_id = get_ObjectId_if_valid(movie_id, 'Movie id')
    return movies.delete_one({"_id": obj_id})
    

def get_movie_by_id(movie_id):
    obj_id = get_ObjectId_if_valid(movie_id, 'Movie id')
    return movies.find_one(obj_id)
    

def search_movie(query):

    filter_query = {}

    sort_query = []

    limit = query.get('limit', None)

    sort_by_attr = query.get('sort_by_attr')
    sort_by_order = query.get('sort_by_order')
    if sort_by_order == 'desc':
        sort_by_order = pymongo.DESCENDING
    else:
        sort_by_order = pymongo.ASCENDING

    if sort_by_attr:    
        sort_query.append((sort_by_attr, sort_by_order))
    else:
        sort_query.append(("name", sort_by_order))
    sort_query.append(("_id", sort_by_order))

    name = query.get('name')
    if name:
        case_insensitive_reg = re.compile(name, re.IGNORECASE)
        filter_query['name'] = case_insensitive_reg

    director = query.get('director')
    if director:
        case_insensitive_reg = re.compile(director, re.IGNORECASE)
        filter_query['director'] = case_insensitive_reg

    genre_to_filter = query.get('genre_to_filter')
    if genre_to_filter:
        genre_filter_operator = query['genre_filter_operator']
        
        if genre_filter_operator == 'and':
            genre_filter_operator = '$all'    
        else:
            genre_filter_operator = '$in'

        filter_query['genre'] = {
            genre_filter_operator : genre_to_filter
        }

    popularity_query = {}

    popularity_min = query.get('popularity_min')
    if popularity_min:
        popularity_query['$gte'] = popularity_min

    popularity_max = query.get('popularity_max')
    if popularity_max:
        popularity_query['$lte'] = popularity_max

    
    if popularity_query:
        filter_query['popularity'] = popularity_query

    imdb_score_query = {}

    imdb_score_min = query.get('imdb_score_min')
    if imdb_score_min:
        imdb_score_query['$gte'] = imdb_score_min

    imdb_score_max = query.get('imdb_score_max')
    if imdb_score_max:
        imdb_score_query['$lte'] = imdb_score_max

    if imdb_score_query:
        filter_query['imdb_score'] = imdb_score_query

    query = {
        '$and' : [
            filter_query
        ]
    }

    print(query)

    if limit:
        return list(movies.find(query).sort(sort_query).limit(limit))
    else:
        return list(movies.find(query).sort(sort_query))