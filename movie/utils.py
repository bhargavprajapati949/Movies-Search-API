addMovieReqSchema = {
    "type": "object",
    "properties": {
        "name": { 
            "type": "string",
            "minLength" : 1
        },
        "imdb_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
        },
        "popularity": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "director": {
            "type": "string",
            "minLength" : 1
        },
        "genre": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "uniqueItems": True
        }
    },
    "additionalProperties": False,
    "required": ["name", "director", "genre"]
}

addBatchMovieReqSchema = { 
    "type" : "array",
    "items": addMovieReqSchema
}

updateMovieReqSchema = {
    "type": "object",
    "properties": {
        "movie_id": {
            "type": "string",
        },
        "name": { 
            "type": "string",
            "minLength" : 1
        },
        "imdb_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
        },
        "popularity": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "director": {
            "type": "string",
            "minLength" : 1
        },
        "genre": {
            "type": "object",
            "properties":{
                "action": {
                    "enum": ["replaceNew", "add", "delete"]
                },
                "data":{
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    },
    "additionalProperties": False,
    "required": ["movie_id"]
}

deleteMovieReqSchema = {
    "type": "object",
    "properties": {
        "movie_id":{
            "type": "string",
        }
    },
    "additionalProperties": False,
    "required": ["movie_id"]
}

searchMovieReqSchema = {
    "type": "object",
    "properties": {
        "limit" : {
            "type": "integer"
        },
        "offset" : {
            "type": "integer"
        },
        "sort" : {
            "type" : "object",
            "properties" : {
                "by_attr": {
                    "type": "string"
                },
                "by_order": {
                    "enum" : ["ascending", "descending"]
                }
            }
        },
        "name": {
            "type": "string"
        },
        "director": {
            "type": "string"
        },
        "genre" : {
            "type": "object",
            "properties": {
                "filter_operator" : {
                    "enum" : ["and", "or"]
                },
                "to_filter": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "popularity" : {
            "type" : "object",
            "properties" : {
                "min" : {
                    "type" : "number",
                    "minimum" : 0,
                    "maximum" : 100
                },
                "max" : {
                    "type" : "number",
                    "minimum" : 0,
                    "maximum" : 100
                }
            }
        },
        "imdb_score" : {
            "type" : "object",
            "properties" : {
                "min" : {
                    "type" : "number",
                    "minimum" : 0,
                    "maximum" : 10
                },
                "max" : {
                    "type" : "number",
                    "minimum" : 0,
                    "maximum" : 10
                }
            }
        }
    },
    "additionalProperties": False
}


def check_numeric(str):
    try:
        float(str)
        return True
    except:
        return False