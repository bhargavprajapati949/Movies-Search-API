import database.movie as db_movies
from errors import BadRequestError, ServerError

class Movie():
    # def __init__(self, name, imdb_score, popularity, director, genre, db_id):
    #     self.id = db_id
    #     self.name = name
    #     self.imdb_score = imdb_score
    #     self.popularity = popularity
    #     self.director = director
    #     self.genre = genre

    def __init__(self, movie):
        if movie.get('_id', None):
            self.id = str(movie.get('_id'))
            movie.pop('_id')
        self.name = movie.get('name')
        self.imdb_score = movie.get('imdb_score')
        self.popularity = movie.get('popularity')
        self.director = movie.get('director')
        self.genre = movie.get('genre')
        self.json_val = movie

    # def __add_id(self, movie_id):
    #     self.id = str(movie_id)

    @staticmethod
    def add_movie(movie_data):
        # movie = Movie(movie_data)
        # insert_res = db_movies.add_movie(movie.json_val)
        insert_res = db_movies.add_movie(movie_data)

        if insert_res:
            try:
                return Movie.get_movie_by_id(insert_res.inserted_id)
            except:
                raise ServerError('Unable to add movie')

        raise ServerError('Unable to add movie')

    def add_batch_movie(movies_list):
        insert_res = db_movies.add_movie_batch(movies_list)

        if insert_res:
            return True

        raise ServerError('Unable to add movies')
                

    @staticmethod
    def update_movie(movie_id, movie_data_updated):
        res = db_movies.update_movie(movie_id, movie_data_updated)
        if res.modified_count == 1:
            return True
        else:
            raise ServerError('Unable to delete movie')

    @staticmethod
    def delete_movie(movie_id):
        res = db_movies.delete_movie(movie_id)
        if res.deleted_count == 1:
            return True
        else:
            raise ServerError('Unable to delete movie')

    @staticmethod
    def search_movie(query_parm):
        return db_movies.search_movie(query_parm)

    @staticmethod
    def get_movie_by_id(movie_id):
        movie = Movie.get_movie_by_id_if_exist(movie_id)
        if movie:
            return movie
        else:
            raise BadRequestError('Movie not found')

    @staticmethod
    def get_movie_by_id_if_exist(movie_id):
        movie = db_movies.get_movie_by_id(movie_id)
        if movie:
            return Movie(movie)
        else:
            return False