# Movies-Search-API

## Table of Contents

- [Introduction](#introduction)
- [Setup Guide](#setup-guide)
- [API Reference](#api-reference)


# [Introduction](#introduction)

This is Movies search API which contains details of various movies. You can make different queries to search movies based on various filters.

### Technology Stack Used
- Python Web Framework - Flask
- MongoDB for storing data
- JWT token for Authentication

### It has two types of access levels.
1. Admin User: This user can add/modify/delete the movies.
2. Normal User: This user can only view the movies.

### Hosted
- This project is hosted on Heroku.
- URL: https://movies-search-api-bhargav.herokuapp.com/
- You can call try experimenting with any endpoints.





# [Setup Guide](#setup-guide)

- Clone the Project on the local PC

- Create Virtual Environment
    ```
    python -m venv <virtual environment name or path>
    ```

- Active Virtual Environment
    - Example Windows
        ```
        .\<virtual environment name or path>\Scripts\activate
        ```

    - Example Linux
        ```
        source ./<virtual environment name or path>/Scripts/activate
        ```


- Install dependencies
    ```
    pip install requirements.txt
    ```
- Add Some Environment Variables
    - You need to add four environment variables
        ```
        DB_URL = <Mongodb Database URI>
        FLASK_ENV = <development OR production>
        SECRET_KEY = <secret key for flask>
        JWT_SECRET_KEY = <secret key for jwt token generation>
        ```

    - Set Environment variable in Linux
        ```
        export <environment variable name>=<environment variable value>
        ```
    - Set Environment variable in Windows
        ```
        set <environment variable name>=<environment variable value>
        ```
    
- Run server
    ```
    flask run
    ```

# [API Reference](#api-reference)

Base URL
```
https://movies-search-api-bhargav.herokuapp.com/
```

### Response Codes
```
200: Success
201: Created
400: Bad request
401: Unauthorized
404: Cannot be found
405: Method not allowed
422: Unprocessable Entity 
50X: Server Error
```

### Example Error Message
```json
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{
    "error" : "{{Error Message}}"
}
```


# EndPoints

## End Points Index
- User Management
    - [Register](#register)
    - [Login](#login)
    - [Profile](#profile)
    - [Delete User](#delete-user)
- Movies
    - [Add Movie](#add-movie)
    - [Update Movie](#update-movie)
    - [Get Movie Detail](#get-movie-detail)
    - [Delete Movie](#delete-movie)
    - [Add Movie in Batch (Add more than one movie in one request)](#add-movie-in-batch-add-more-than-one-movie-in-one-request)
    - [⭐Movie Search EndPoint⭐](#movie-search-endpoint)


## Register

End Point: 
```
POST /user/register
```

**Detail** 
- Anyone can register on the platform using this API endpoint.

**You send**
- Email id, Password, and Name

**Request Parameters**

| Property | Description | Type | Is Required |
| --- | --- | --- | --- |
| name | User Name | String | True |
| email | Email | Email | True |
| password | Password | String | True |
| is_admin | If the user wants to register as admin make it True | Boolean | False |

**Password Constrains**

*   Password should be of Minimum of eight characters,
*   at least one uppercase letter
*   one lowercase letter
*   one number and
*   one special character (@$!%*#?&)

**Action**
- If email is not already used by another user then an account will be created

**Sample Request:**
```json
POST /user/register
Content-Type: application/json

{
    "name" : "Wanda Maximoff",
    "email" : "wandaMaximoff@gmail.com",
    "password" : "Scarlet@Witch9",
    "is_admin" : true
}
```

**Successful Response:**
```json
HTTP/1.1 201 CREATED
Content-Type: application/json
 
{
    "email" : "wandaMaximoff@gmail.com",
    "id" : "{{user_id}}",
    "name" : "Wanda Maximoff"
}

```


## Login
End Point

```
POST /user/login
```

**You send** 
- Your  login credentials.

**Request Parameters**

| Property | Type | Required |
| --- | --- | --- |
| email | Email | True |
| password | String | True |

**You get:** 
- A `JWT API Token` with which you can take further actions.


**Sample Request**
```json
POST /user/login
Content-Type: application/json
 
{
    "email" : "wandaMaximoff@gmail.com",
    "password" : "Scarlet@Witch9"
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "access_token" : "{{api_token}}"
}
```


## Profile

End Point:
```
GET /user/profile
```

**You send**
- Authentication Token in Header.

**You get** 
- User's all personal information.

**Sample Request**
```json
GET /user/profile
Authorization: Bearer {{api_token}}
```

**Successful Response**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "email" : "wandaMaximoff@gmail.com",
    "id" : "{{user_id}}",
    "name" : "Wanda Maximoff"
}

```


## Delete User

End Point:
```
DELETE /user/delete
```

**You send**
- Authentication Token in Header.

**Action** 
- The user will be deleted from the database.

**Sample Request:**
```json
DELETE /user/delete
Authorization: Bearer {{api_token}}
```

**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "message" : "User Deleted"
}
```

## Add Movie

End Point:
```
POST /movie/add
```

**You send:**  
- Authentication Token of user with admin access in Header.
- Movie information in JSON format

**Request Parameters**

| Property | Type | Is Required |
| --- | --- | --- |
| name | String | True |
| director | String | True |
| popularity | Number | False |
| imdb_score | Number | False |
| genre | List of Strings | True |


**Action:**
- If all information is valid then the movie will be added to the database.

**Sample Request:**
```json
POST /movie/add
Authorization: Bearer {{api_token}}
Content-Type: application/json

{
    "popularity" : 70.0,
    "director" : "Sam Raimi",
    "genre" : [
        "Action",
        "Adventure",
        "Fantasy",
        "Super Hero"
    ],
    "imdb_score" : 7.0,
    "name" : "Doctor Strange in the Multiverse of Madness"
}
```

**Successful Response:**
```json
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "_id" : "{{movie_id}}",
    "director" : "Sam Raimi",
    "genre" : [
        "Action",
        "Adventure",
        "Fantasy",
        "Super Hero"
    ],
    "imdb_score" : 7.0,
    "name" : "Doctor Strange in the Multiverse of Madness",
    "popularity" : 70.0
}
```


## Update Movie

End Point:
```
PUT /movie/update
```

**You send:**  
- Authentication Token of user with admin access in Header.
- Information of Movie that needs to update in JSON format

**Request Parameters**

| Property | Type | Is Required |
| --- | --- | --- |
| movie_id | String | True |
| name | String | False |
| director | String | False |
| popularity | Number | False |
| imdb_score | Number | False |
| genre | JSON object with action and data | False |

JSON format of the genre

| Property | Allowed Values |
|--- | --- |
| action | "replaceNew", "add", "delete" | 
| data | List of Strings |

Details about genre actions
- ReplaceNew: Delete all existing genre values and add new ones provided in the data
- add: Add New genre values provided in the data
- delete: Delete genre values provided in data from existing values

Provide only those parameters, which you want to update for given movie_id

**Action:**
- Update details for the movie identified my `movie_id`   

**Sample Request:**
```json
PUT /movie/update
Authorization: Bearer {{api_token}}
Content-Type: application/json
 
{
    "movie_id": "{{movie_id}}",
    "popularity": 90.0,
    "genre": {
        "action": "delete",
        "data": [
            "Super Hero"
        ]
    }
}
```

**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "message":"movie updated"
}
```



## Get Movie Detail

End Point:
```
GET /movie/{{movie_id}}
```

**You send**
- Movie Id in URL argument

**You get** 
- Movie details for passed Movie Id

**Sample Request**
```json
GET /movie/{{movie_id}}
```

**Successful Response**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "_id":"{{movie_id}}",
    "director":"Sam Raimi",
    "genre":[
        "Action",
        "Adventure",
        "Fantasy"
    ],
    "imdb_score":7.0,
    "name":"Doctor Strange in the Multiverse of Madness",
    "popularity":90.0
}
```


## Delete Movie

End Point:
```
DELETE /movie/delete
```

**You send**
- Authentication Token of user with admin access in Header.
- Movie Id which you want to delete

**Request Parameters**

| Property | **Type** | **Required** |
| --- | --- | --- |
| movie_id | String | True |


**Action** 
- The movie will be deleted from the database.

**Sample Request:**
```json
DELETE /movie/delete HTTP/1.1
Authorization: Bearer {{api_token}}
{
    "movie_id" : "{{movie_id}}"
}
```

**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "message" : "Movie Deleted"
}
```


## Add Movie in Batch (Add more than one movie in one request)


End Point:
```
POST /movie/addBatch
```

**You send:**  
- Authentication Token of user with admin access in Header.
- List of Movie information in JSON format

**Action:**
- If the details of all movies are valid then all movies will be added to the database.

**Sample Request:**
```json
POST /movie/addBatch
Authorization: Bearer {{api_token}}
Content-Type: application/json
 
[
    {
        "popularity": 84.0,
        "director": "Joe Russo",
        "genre": [
            "Action",
            "Adventure",
            "Sci-Fi"
        ],
        "imdb_score": 8.4,
        "name": "Avengers: Infinity War"
    },
    {
        "popularity": 84.0,
        "director": "Anthony Russo",
        "genre": [
            "Action",
            "Adventure",
            "Drama"
        ],
        "imdb_score": 8.4,
        "name": "Avengers: Endgame"
    }
]
```

**Successful Response:**
```json
HTTP/1.1 201 CREATED
Content-Type: application/json
 
{
    "data" : [
        {
            "_id" : "{{movie_id}}",
            "director" : "Joe Russo",
            "genre" : [
                "Action",
                "Adventure",
                "Sci-Fi"
            ],
            "imdb_score" : 8.4,
            "name" : "Avengers: Infinity War",
            "popularity" : 84.0
        },
        {
            "_id" : "{{movie_id}}",
            "director":"Anthony Russo",
            "genre" : [
                "Action",
                "Adventure",
                "Drama"
            ],
            "imdb_score" : 8.4,
            "name" : "Avengers: Endgame",
            "popularity" : 84.0
        }
    ]
}
```


## Movie Search EndPoint

End Point:
```
GET /movie
```

**You send**
- Different Query parameters in URL

**Query Parameters**

| Parameter | Type | **Permitted Values** | **Description** |
| --- | --- | --- | --- |
| limit | Integer |  | Limit the number of result in response |
| sort_by_attr | String | "name", "director", "popularity",  <br>"imdb_score" | To sort result according to specific attribute |
| sort_by_order | String | "ascending", "descending" | To sort result in ascending or descending order |
| name | String |  | Search with name field |
| director | String |  | Search with director field |
| genre_filter_operator | String | "and": give result if all genre from query exist in movie  <br>"or": give result if any genre from query exist in movie | Search with genre field |
| genre_to_filter | String |  | Search with genre field |
| popularity_min | Number |  | Give Results with popularity greater than or equal to popularity_min |
| popularity_max | Number |  | Give Results with popularity less than or equal to popularity_max |
| imdb_score_min | Number |  | Give Results with imdb_score greater than or equal to imdb_score_min |
| imdb_score_max | Number |  | Give Results with imdb_score less than or equal to imdb_score_max |

All values are optional


**You get** 
- Movie details of all filtered movies

**Sample Request**
```
GET /movie?limit=5&sort_by_attr=director&sort_by_order=descending&name=avengers&director=russo&genre_filter_operator=and&genre_to_filter=Action&genre_to_filter=Adventure&popularity_min=60&popularity_max=85&imdb_score_min=6.0&imdb_score_max=8.5
```

**Beautified Sample Request**
```
GET /movie?
    limit=5&
    sort_by_attr=director&
    sort_by_order=descending&
    name=avengers&
    director=russo&
    genre_filter_operator=and&
    genre_to_filter=Action&
    genre_to_filter=Adventure&
    popularity_min=60&
    popularity_max=85&
    imdb_score_min=6.0&
    imdb_score_max=8.5
```


**Successful Response**
```json
HTTP/1.1 200 OK
Content-Type: application/json
 
{
    "result" : [
        {
            "_id" : "{{movie_id}}",
            "director" : "Joe Russo",
            "genre" : [
                "Action",
                "Adventure",
                "Sci-Fi"
            ],
            "imdb_score" : 8.4,
            "name" : "Avengers: Infinity War",
            "popularity" : 84.0
        },
        {
            "_id" : "{{movie_id}}",
            "director" : "Anthony Russo",
            "genre" : [
                "Action",
                "Adventure",
                "Drama"
            ],
            "imdb_score" : 8.4,
            "name" : "Avengers: Endgame",
            "popularity" : 84.0
        }
    ]
}
```